import os
import shutil
from datetime import datetime
from lxml import etree
from flask import current_app
from app.services.validator import XMLValidator
from app.services.rdf_graph import SemanticEngine

class XMLRepository:
    def __init__(self, entidad="alumnos"):
        self.entidad = entidad
        self.campos_esperados = ['nombre', 'apellidos', 'correo', 'carrera_id', 'semestre', 'promedio', 'estatus']
    
    def _get_file_path(self):
        xml_dir = current_app.config.get('XML_DIR', 'data/xml') if current_app else 'data/xml'
        return os.path.join(xml_dir, f'{self.entidad}.xml')
        
    def _crear_backup(self, xml_path):
        """Crea una copia del XML en data/backups/ antes de cualquier escritura."""
        backup_dir = os.path.join('data', 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
        backup_path = os.path.join(backup_dir, f'{self.entidad}_{timestamp}.xml')
        
        if os.path.exists(xml_path):
            shutil.copy2(xml_path, backup_path)

    def _guardar_xml(self, tree, xml_path):
        """Valida el árbol contra XSD y DTD, crea un backup, guarda el archivo y actualiza el RDF."""
        xsd_path = os.path.join('schemas', 'xsd', f'{self.entidad}.xsd')
        dtd_path = os.path.join('schemas', 'dtd', f'{self.entidad}.dtd')
        
        # 1. Validar integridad de datos
        XMLValidator.validar_contra_xsd(tree, xsd_path)
        XMLValidator.validar_contra_dtd(tree, dtd_path)
        
        # 2. Crear respaldo
        self._crear_backup(xml_path)
        
        # 3. Guardar el archivo definitivo XML preservando el DOCTYPE
        doctype = f'<!DOCTYPE {self.entidad} SYSTEM "../../schemas/dtd/{self.entidad}.dtd">'
        tree.write(xml_path, encoding="UTF-8", xml_declaration=True, pretty_print=True, doctype=doctype)
        
        # 4. Reconstruir el grafo semántico inmediatamente después de guardar
        SemanticEngine.construir_grafo()

    # ==========================
    # Operaciones CRUD Alumnos
    # ==========================
    def listar_alumnos(self):
        """Retorna una lista de diccionarios (útil para la API JSON)."""
        xml_path = self._get_file_path()
        if not os.path.exists(xml_path):
            return []
            
        tree = etree.parse(xml_path)
        alumnos = []
        for nodo in tree.xpath('//alumno'):
            alumno_data = {"id": nodo.get("id"), "matricula": nodo.get("matricula")}
            for hijo in nodo:
                alumno_data[hijo.tag] = hijo.text
            alumnos.append(alumno_data)
        return alumnos

    def agregar_alumno(self, datos):
        xml_path = self._get_file_path()
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_path, parser)
        root = tree.getroot()
        
        if root.xpath(f"//alumno[@id='{datos['id']}']"):
            raise ValueError(f"El alumno con ID {datos['id']} ya existe.")
            
        nuevo_alumno = etree.Element("alumno", id=datos['id'], matricula=datos['matricula'])
        
        for campo in self.campos_esperados:
            hijo = etree.Element(campo)
            hijo.text = str(datos.get(campo, ''))
            nuevo_alumno.append(hijo)
            
        root.append(nuevo_alumno)
        self._guardar_xml(tree, xml_path)
        return datos

    def eliminar_alumno(self, alumno_id):
        xml_path = self._get_file_path()
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_path, parser)
        root = tree.getroot()
        
        nodos = root.xpath(f"//alumno[@id='{alumno_id}']")
        if not nodos:
            return False
            
        root.remove(nodos[0])
        self._guardar_xml(tree, xml_path)
        return True

    # ==========================
    # Operaciones CRUD Materias
    # ==========================
    def listar_materias(self):
        """Retorna el catálogo de materias en formato lista de diccionarios."""
        xml_path = self._get_file_path()
        if not os.path.exists(xml_path):
            return []

        tree = etree.parse(xml_path)
        materias = []
        for m in tree.xpath('//materia'):
            carrera_nodo = m.find('carrera')
            profesor_nodo = m.find('profesor')
            materias.append({
                "id": m.get("id"),
                "clave": m.get("clave"),
                "nombre": (m.findtext("nombre") or "").strip(),
                "descripcion": (m.findtext("descripcion") or "").strip(),
                "creditos": int((m.findtext("creditos") or "0").strip()),
                "semestre": int((m.findtext("semestre") or "0").strip()),
                "carrera_codigo": carrera_nodo.get("codigo") if carrera_nodo is not None else "",
                "carrera": (m.findtext("carrera") or "").strip(),
                "profesor_id": profesor_nodo.get("id") if profesor_nodo is not None else "",
                "profesor": (m.findtext("profesor") or "").strip(),
                "prerrequisitos": [
                    {"ref": p.get("ref"), "nombre": p.get("nombre")}
                    for p in m.xpath("prerrequisitos/prerrequisito")
                ]
            })
        return materias

    def agregar_materia(self, datos):
        """Agrega una nueva materia validando IDs, IDREFs, DTD y XSD."""
        xml_path = self._get_file_path()
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_path, parser)
        root = tree.getroot()

        materia_id = str(datos.get("id", "")).strip().upper()
        clave = str(datos.get("clave", "")).strip().upper()

        if root.xpath(f"//materia[@id='{materia_id}']"):
            raise ValueError(f"La materia con ID '{materia_id}' ya existe.")

        nueva = etree.Element("materia", id=materia_id, clave=clave)
        etree.SubElement(nueva, "nombre").text = str(datos.get("nombre", "")).strip()
        etree.SubElement(nueva, "descripcion").text = str(datos.get("descripcion", "")).strip()
        etree.SubElement(nueva, "creditos").text = str(datos.get("creditos", "6")).strip()
        etree.SubElement(nueva, "semestre").text = str(datos.get("semestre", "1")).strip()

        carrera_el = etree.SubElement(
            nueva, "carrera", codigo=str(datos.get("carrera_codigo", "ICC")).strip().upper()
        )
        carrera_el.text = str(
            datos.get("carrera_nombre", "Ingeniería en Ciencias de la Computación")
        ).strip()

        profesor_el = etree.SubElement(
            nueva, "profesor", id=str(datos.get("profesor_id", "P001")).strip().upper()
        )
        profesor_el.text = str(datos.get("profesor_nombre", "")).strip()

        prerreq_el = etree.SubElement(nueva, "prerrequisitos")
        prerreqs = datos.get("prerrequisitos", [])
        if isinstance(prerreqs, str):
            prerreqs = [r.strip() for r in prerreqs.split(",") if r.strip()]

        for ref_id in prerreqs:
            nodo_ref = root.xpath(f"//materia[@id='{ref_id}']")
            nombre_ref = (nodo_ref[0].findtext("nombre") or "").strip() if nodo_ref else ref_id
            etree.SubElement(prerreq_el, "prerrequisito", ref=ref_id, nombre=nombre_ref)

        root.append(nueva)
        self._guardar_xml(tree, xml_path)
        return datos

    def eliminar_materia(self, materia_id):
        """Elimina una materia verificando antes que no deje un IDREF huérfano en otra materia."""
        xml_path = self._get_file_path()
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_path, parser)
        root = tree.getroot()

        dependientes = root.xpath(
            f"//materia[prerrequisitos/prerrequisito[@ref='{materia_id}']]/@id"
        )
        if dependientes:
            raise ValueError(
                f"No se puede eliminar {materia_id} porque es prerrequisito de: {', '.join(dependientes)}"
            )

        nodos = root.xpath(f"//materia[@id='{materia_id}']")
        if not nodos:
            return False

        root.remove(nodos[0])
        self._guardar_xml(tree, xml_path)
        return True