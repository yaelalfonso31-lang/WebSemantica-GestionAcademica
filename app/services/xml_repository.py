import os
from lxml import etree

class XMLRepository:
    def __init__(self, base_xml_dir="data/xml"):
        self.base_xml_dir = base_xml_dir

    def _get_path(self, filename):
        return os.path.join(self.base_xml_dir, filename)

    def get_tree(self, filename):
        path = self._get_path(filename)
        parser = etree.XMLParser(remove_blank_text=True)
        return etree.parse(path, parser)

    def listar_alumnos(self):
        tree = self.get_tree("alumnos.xml")
        root = tree.getroot()
        alumnos = []
        for elem in root.findall("alumno"):
            alumnos.append({
                "id": elem.get("id"),
                "matricula": elem.get("matricula"),
                "nombre": elem.findtext("nombre", default=""),
                "apellidos": elem.findtext("apellidos", default=""),
                "correo": elem.findtext("correo", default=""),
                "carrera_id": elem.findtext("carrera_id", default=""),
                "semestre": elem.findtext("semestre", default="1"),
                "promedio": elem.findtext("promedio", default="0.0"),
                "estatus": elem.findtext("estatus", default="Activo"),
            })
        return alumnos

    def obtener_alumno(self, alumno_id):
        tree = self.get_tree("alumnos.xml")
        elem = tree.find(f"//alumno[@id='{alumno_id}']")
        if elem is None:
            return None
        return {
            "id": elem.get("id"),
            "matricula": elem.get("matricula"),
            "nombre": elem.findtext("nombre", default=""),
            "apellidos": elem.findtext("apellidos", default=""),
            "correo": elem.findtext("correo", default=""),
            "carrera_id": elem.findtext("carrera_id", default=""),
            "semestre": elem.findtext("semestre", default="1"),
            "promedio": elem.findtext("promedio", default="0.0"),
            "estatus": elem.findtext("estatus", default="Activo"),
        }

    def agregar_alumno(self, datos):
        path = self._get_path("alumnos.xml")
        tree = self.get_tree("alumnos.xml")
        root = tree.getroot()

        if root.find(f"alumno[@id='{datos['id']}']") is not None:
            raise ValueError(f"El alumno con ID {datos['id']} ya existe.")

        nuevo = etree.SubElement(root, "alumno", id=datos["id"], matricula=datos["matricula"])
        for campo in ["nombre", "apellidos", "correo", "carrera_id", "semestre", "promedio", "estatus"]:
            sub = etree.SubElement(nuevo, campo)
            sub.text = str(datos.get(campo, ""))

        tree.write(path, pretty_print=True, xml_declaration=True, encoding="UTF-8")
        return datos

    def actualizar_alumno(self, alumno_id, datos):
        path = self._get_path("alumnos.xml")
        tree = self.get_tree("alumnos.xml")
        root = tree.getroot()
        elem = root.find(f"alumno[@id='{alumno_id}']")
        if elem is None:
            raise ValueError(f"Alumno {alumno_id} no encontrado.")

        if "matricula" in datos:
            elem.set("matricula", str(datos["matricula"]))

        for campo in ["nombre", "apellidos", "correo", "carrera_id", "semestre", "promedio", "estatus"]:
            if campo in datos:
                nodo = elem.find(campo)
                if nodo is None:
                    nodo = etree.SubElement(elem, campo)
                nodo.text = str(datos[campo])

        tree.write(path, pretty_print=True, xml_declaration=True, encoding="UTF-8")
        return self.obtener_alumno(alumno_id)

    def eliminar_alumno(self, alumno_id):
        path = self._get_path("alumnos.xml")
        tree = self.get_tree("alumnos.xml")
        root = tree.getroot()
        elem = root.find(f"alumno[@id='{alumno_id}']")
        if elem is None:
            return False
        root.remove(elem)
        tree.write(path, pretty_print=True, xml_declaration=True, encoding="UTF-8")
        return True