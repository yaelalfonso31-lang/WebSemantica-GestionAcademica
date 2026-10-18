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
        return os.path.join(current_app.config.get('XML_DIR', 'data/xml'), f'{self.entidad}.xml')
        
    def _crear_backup(self, xml_path):
        """Crea una copia del XML en data/backups/ antes de cualquier escritura."""
        backup_dir = os.path.join('data', 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
        backup_path = os.path.join(backup_dir, f'{self.entidad}_{timestamp}.xml')
        
        if os.path.exists(xml_path):
            shutil.copy2(xml_path, backup_path)
            
    def _guardar_xml(self, tree, xml_path):
        """Valida el árbol contra DTD y XSD, crea un backup y guarda el archivo."""
        xsd_path = os.path.join('schemas', 'xsd', f'{self.entidad}.xsd')
        dtd_path = os.path.join('schemas', 'dtd', f'{self.entidad}.dtd')
        
        # 1. Validar integridad de datos
        XMLValidator.validar_contra_xsd(tree, xsd_path)
        XMLValidator.validar_contra_dtd(tree, dtd_path)
        
        # 2. Crear respaldo
        self._crear_backup(xml_path)
        
        # 3. Guardar el archivo definitivo (preservando el DOCTYPE si es posible)
        doctype = f'<!DOCTYPE {self.entidad} SYSTEM "../../schemas/dtd/{self.entidad}.dtd">'
        tree.write(xml_path, encoding="UTF-8", xml_declaration=True, pretty_print=True, doctype=doctype)

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
        tree = etree.parse(xml_path)
        root = tree.getroot()
        
        # Verificar que el ID o la matrícula no existan ya
        if root.xpath(f"//alumno[@id='{datos['id']}']"):
            raise ValueError(f"El alumno con ID {datos['id']} ya existe.")
            
        # Crear el nodo principal
        nuevo_alumno = etree.Element("alumno", id=datos['id'], matricula=datos['matricula'])
        
        # Agregar los hijos según los campos esperados
        for campo in self.campos_esperados:
            hijo = etree.Element(campo)
            hijo.text = str(datos.get(campo, ''))
            nuevo_alumno.append(hijo)
            
        root.append(nuevo_alumno)
        self._guardar_xml(tree, xml_path)
        return datos

    def eliminar_alumno(self, alumno_id):
        xml_path = self._get_file_path()
        tree = etree.parse(xml_path)
        root = tree.getroot()
        
        nodos = root.xpath(f"//alumno[@id='{alumno_id}']")
        if not nodos:
            return False
            
        root.remove(nodos[0])
        self._guardar_xml(tree, xml_path)
        return True

    def _guardar_xml(self, tree, xml_path):
        """Valida el árbol, crea un backup, guarda el archivo y actualiza el RDF."""
        xsd_path = os.path.join('schemas', 'xsd', f'{self.entidad}.xsd')
        dtd_path = os.path.join('schemas', 'dtd', f'{self.entidad}.dtd')
        
        # 1. Validar integridad de datos
        XMLValidator.validar_contra_xsd(tree, xsd_path)
        XMLValidator.validar_contra_dtd(tree, dtd_path)
        
        # 2. Crear respaldo
        self._crear_backup(xml_path)
        
        # 3. Guardar el archivo definitivo XML
        doctype = f'<!DOCTYPE {self.entidad} SYSTEM "../../schemas/dtd/{self.entidad}.dtd">'
        tree.write(xml_path, encoding="UTF-8", xml_declaration=True, pretty_print=True, doctype=doctype)
        
        # 4. ¡NUEVO!: Reconstruir el grafo semántico inmediatamente después de guardar
        SemanticEngine.construir_grafo()

    
    # ==========================
    # Operaciones CRUD Profesores
    # ==========================
    def listar_profesores(self):
        """Retorna profesores con el código y nombre de cada materia."""
        xml_path = self._get_file_path()

        if not os.path.exists(xml_path):
            return []

        tree = etree.parse(xml_path)
        profesores = []

        for nodo in tree.getroot().findall("profesor"):
            profesor = {
                "id": nodo.get("id"),
                "nombre": nodo.findtext("nombre", default=""),
                "especialidad": nodo.findtext("especialidad", default=""),
                "correo": nodo.findtext("correo", default=""),
                "departamento": nodo.findtext("departamento", default=""),
                "materias_impartidas": [
                    {
                        "codigo": materia.get("codigo", ""),
                        "nombre": materia.text or ""
                    }
                    for materia in nodo.findall(
                        "materias_impartidas/materia"
                    )
                ]
            }
            profesores.append(profesor)

        return profesores


    def obtener_profesor(self, profesor_id):
        """Busca un profesor por su atributo ID."""
        for profesor in self.listar_profesores():
            if profesor["id"] == profesor_id:
                return profesor

        return None

    
    def agregar_profesor(self, datos):
        """Registra un profesor y sus materias, validando el XML."""
        campos = [
            "id", "nombre", "especialidad", "correo", "departamento"
        ]

        for campo in campos:
            if not isinstance(datos.get(campo), str) or not datos[campo].strip():
                raise ValueError(f"El campo '{campo}' es obligatorio.")

        profesor_id = datos["id"].strip()
        materias = datos.get("materias_impartidas", [])

        if not isinstance(materias, list):
            raise ValueError("'materias_impartidas' debe ser una lista.")

        for materia in materias:
            if not isinstance(materia, dict):
                raise ValueError("Cada materia debe ser un objeto.")

            codigo = materia.get("codigo")
            nombre = materia.get("nombre")

            if not isinstance(codigo, str) or not codigo.strip():
                raise ValueError("Cada materia debe tener un código válido.")

            if not isinstance(nombre, str) or not nombre.strip():
                raise ValueError("Cada materia debe tener un nombre.")

        xml_path = self._get_file_path()

        if not os.path.exists(xml_path):
            raise ValueError(
                "No existe profesores.xml. Verifica la ruta del catálogo."
            )

        tree = etree.parse(xml_path)
        root = tree.getroot()

        if any(p.get("id") == profesor_id for p in root.findall("profesor")):
            raise ValueError(f"El profesor con ID {profesor_id} ya existe.")

        nuevo = etree.SubElement(root, "profesor", id=profesor_id)

        for campo in campos[1:]:
            hijo = etree.SubElement(nuevo, campo)
            hijo.text = datos[campo].strip()

        materias_xml = etree.SubElement(nuevo, "materias_impartidas")

        for materia in materias:
            elemento = etree.SubElement(
                materias_xml,
                "materia",
                codigo=materia["codigo"].strip()
            )
            elemento.text = materia["nombre"].strip()

        self._guardar_xml(tree, xml_path)
        return self.obtener_profesor(profesor_id)


    def actualizar_profesor(self, profesor_id, datos):
        """Actualiza los datos de un profesor existente."""
        xml_path = self._get_file_path()

        if not os.path.exists(xml_path):
            return None

        tree = etree.parse(xml_path)
        root = tree.getroot()

        nodo = next(
            (
                p for p in root.findall("profesor")
                if p.get("id") == profesor_id
            ),
            None
        )

        if nodo is None:
            return None

        campos = [
            "nombre", "especialidad", "correo", "departamento"
        ]

        for campo in campos:
            if campo in datos:
                valor = datos[campo]

                if not isinstance(valor, str) or not valor.strip():
                    raise ValueError(
                        f"El campo '{campo}' no puede estar vacío."
                    )

                nodo.find(campo).text = valor.strip()

        if "materias_impartidas" in datos:
            materias = datos["materias_impartidas"]

            if not isinstance(materias, list):
                raise ValueError(
                    "'materias_impartidas' debe ser una lista."
                )

            for materia in materias:
                if not isinstance(materia, dict):
                    raise ValueError("Cada materia debe ser un objeto.")

                codigo = materia.get("codigo")
                nombre = materia.get("nombre")

                if not isinstance(codigo, str) or not codigo.strip():
                    raise ValueError("Cada materia debe tener un código válido.")

                if not isinstance(nombre, str) or not nombre.strip():
                    raise ValueError("Cada materia debe tener un nombre.")

            materias_xml = nodo.find("materias_impartidas")

            if materias_xml is None:
                materias_xml = etree.SubElement(nodo, "materias_impartidas")

            for materia in list(materias_xml):
                materias_xml.remove(materia)

            for materia in materias:
                elemento = etree.SubElement(
                    materias_xml,
                    "materia",
                    codigo=materia["codigo"].strip()
                )
                elemento.text = materia["nombre"].strip()


        self._guardar_xml(tree, xml_path)
        return self.obtener_profesor(profesor_id)

    def eliminar_profesor(self, profesor_id):
        """Elimina un profesor por su atributo ID."""
        xml_path = self._get_file_path()

        if not os.path.exists(xml_path):
            return False

        tree = etree.parse(xml_path)
        root = tree.getroot()

        nodo = next(
            (
                p for p in root.findall("profesor")
                if p.get("id") == profesor_id
            ),
            None
        )

        if nodo is None:
            return False

        root.remove(nodo)
        self._guardar_xml(tree, xml_path)
        return True
