from flask import Blueprint, flash, jsonify, redirect, request, session, url_for

from app.auth.decorators import login_requerido, rol_requerido
from app.services import academic_metrics as metricas
from app.services.transformer import transformar_a_html
from app.services.xml_repository import LOCK_ESCRITURA, XMLRepository
from app.services.xml_utils import cargar, ruta_xml, texto, xpath
from lxml import etree

calificaciones_bp = Blueprint('calificaciones', __name__)


@calificaciones_bp.route('/calificar', methods=['GET'])
@login_requerido
@rol_requerido('profesor')
def vista_calificar():
    profesor_id = session.get('ref_id')
    grupo_id = request.args.get('grupo', '').strip()

    if not grupo_id:
        # Sin grupo no hay nada que calificar: si solo tiene uno vamos directo, si no, que elija
        propios = metricas.grupos_de_profesor(profesor_id)
        if len(propios) == 1:
            return redirect(url_for('calificaciones.vista_calificar', grupo=propios[0].get('id')))
        flash('Elige el grupo que quieres calificar.', 'info')
        return redirect(url_for('grupos.vista_mis_grupos'))

    grupo = metricas.grupo_de_profesor(profesor_id, grupo_id)
    if grupo is None:  # no existe o es de otro profesor
        flash('Ese grupo no existe o no está asignado a ti.', 'danger')
        return redirect(url_for('grupos.vista_mis_grupos'))

    return transformar_a_html(
        xml_path_or_string=metricas.xml_evaluacion(grupo),
        xslt_filename='calificaciones.xsl',
        params={'rol_usuario': session.get('rol'),
                'nombre_usuario': session.get('nombre') or session.get('username')},
    )


@calificaciones_bp.route('/api/calificar', methods=['POST'])
@login_requerido
@rol_requerido('profesor')
def guardar_calificaciones():
    """Recibe {"grupo": "G-...", "calificaciones": {"I001": "90", "I002": ""}}.

    El estatus se deriva de la calificación (>= mínima aprueba); el profesor solo puede
    modificar inscripciones de sus propios grupos; todo se valida antes de escribir.
    """
    datos = request.get_json(silent=True) or {}
    grupo = metricas.grupo_de_profesor(session.get('ref_id'), str(datos.get('grupo', '')))
    califs = datos.get('calificaciones')
    if grupo is None:
        return jsonify({'error': 'El grupo no existe o no está asignado a ti.'}), 403
    if not isinstance(califs, dict) or not califs:
        return jsonify({'error': 'No se recibieron calificaciones.'}), 400

    with LOCK_ESCRITURA:
        arbol = cargar('inscripciones')
        if arbol is None:
            return jsonify({'error': 'No se encontró la base de datos de inscripciones.'}), 404
        permitidas = {i.get('id'): i for i in metricas.inscripciones_de_grupo(grupo, arbol)}

        # 1) Validar TODO antes de modificar nada
        nuevas, errores = {}, []
        for insc_id, valor in califs.items():
            if insc_id not in permitidas:
                errores.append(f'{insc_id}: no pertenece a tu grupo.')
                continue
            try:
                nuevas[insc_id] = metricas.parsear_calificacion(valor)
            except ValueError as e:
                errores.append(f'{insc_id}: {e}')
        if errores:
            return jsonify({'error': 'No se guardó nada. ' + ' '.join(errores)}), 400

        # 2) Aplicar cambios respetando el orden que exige el XSD (calificacion_final antes de estatus)
        for insc_id, cal in nuevas.items():
            nodo = permitidas[insc_id]
            calif_node = nodo.find('calificacion_final')
            estatus_node = nodo.find('estatus')
            if cal is None:
                if calif_node is not None:
                    nodo.remove(calif_node)
                estatus_node.text = 'Cursando'
                continue
            if calif_node is None:
                calif_node = etree.Element('calificacion_final')
                estatus_node.addprevious(calif_node)
            calif_node.text = str(cal)
            estatus_node.text = metricas.estatus_por_calificacion(cal)

        # 3) Guardar con validación XSD/DTD + respaldo; mantener alumnos.promedio al día
        try:
            XMLRepository('inscripciones')._guardar_xml(arbol, ruta_xml('inscripciones'), reconstruir_grafo=False)
            _actualizar_promedios({texto(permitidas[i], 'alumno_id') for i in nuevas}, arbol)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

    return jsonify({'mensaje': f'{len(nuevas)} calificación(es) guardada(s) y grafo RDF actualizado.'})


def _actualizar_promedios(alumnos_ids, inscripciones):
    """Recalcula alumnos.promedio (lo usan SPARQL y el dashboard) y reconstruye el grafo una vez."""
    alumnos = cargar('alumnos')
    for aid in alumnos_ids:
        promedio = metricas.promedio_de(aid, inscripciones)
        nodo = xpath(alumnos, '//alumno[@id=$a]', a=aid)
        if promedio is not None and nodo:
            nodo[0].find('promedio').text = str(promedio)
    XMLRepository('alumnos')._guardar_xml(alumnos, ruta_xml('alumnos'))  # reconstruye el grafo
