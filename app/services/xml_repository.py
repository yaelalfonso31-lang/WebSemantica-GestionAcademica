
import os
import shutil
import threading
from datetime import datetime

from lxml import etree
from flask import current_app

from app.services.validator import XMLValidator
from app.services.paths import ruta
from app.services.rdf_graph import SemanticEngine

# Serializa los ciclos leer-modificar-guardar sobre los XML (un solo proceso).
LOCK_ESCRITURA = threading.RLock()


class XMLRepository:
    def __init__(self, entidad="alumnos"):
        self.entidad = entidad
        self.campos_esperados = [
            "nombre",
            "apellidos",
            "correo",
            "carrera_id",
            "semestre",
            "promedio",
            "estatus",
        ]

    def _get_file_path(self):
        try:
            xml_dir = current_app.config.get("XML_DIR", "data/xml")
        except RuntimeError:
            xml_dir = "data/xml"

        return os.path.join(xml_dir, f"{self.entidad}.xml")

    def _crear_backup(self, xml_path):
        """Crea una copia del XML antes de cualquier escritura."""
        backup_dir = ruta("BACKUP_DIR")
        os.makedirs(backup_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        backup_path = os.path.join(
            backup_dir, f"{self.entidad}_{timestamp}.xml"
        )

        if os.path.exists(xml_path):
            shutil.copy2(xml_path, backup_path)

    def _guardar_xml(self, tree, xml_path, reconstruir_grafo=True):
        """Valida con XSD y DTD, respalda, guarda y actualiza el RDF."""
        xsd_path = ruta("SCHEMAS_DIR", "xsd", f"{self.entidad}.xsd")
        dtd_path = ruta("SCHEMAS_DIR", "dtd", f"{self.entidad}.dtd")

        XMLValidator.validar_contra_xsd(tree, xsd_path)
        XMLValidator.validar_contra_dtd(tree, dtd_path)

        self._crear_backup(xml_path)

        doctype = (
            f'<!DOCTYPE {self.entidad} '
            f'SYSTEM "../../schemas/dtd/{self.entidad}.dtd">'
        )

        tmp_path = xml_path + ".tmp"
        tree.write(
            tmp_path,
            encoding="UTF-8",
            xml_declaration=True,
            pretty_print=True,
            doctype=doctype,
        )
        os.replace(tmp_path, xml_path)  # atómico: nunca queda un XML a medio escribir

        if reconstruir_grafo:
            SemanticEngine.construir_grafo()

    # ==========================
    # Operaciones CRUD Alumnos
    # ==========================

    def listar_alumnos(self):
        """Retorna los alumnos como una lista de diccionarios."""
        xml_path = self._get_file_path()

        if not os.path.exists(xml_path):
            return []

        tree = etree.parse(xml_path)
        alumnos = []

        for nodo in tree.xpath("//alumno"):
            alumno_data = {
                "id": nodo.get("id"),
                "matricula": nodo.get("matricula"),
            }

            for hijo in nodo:
                alumno_data[hijo.tag] = hijo.text

            alumnos.append(alumno_data)

        return alumnos

    def agregar_alumno(self, datos):
        xml_path = self._get_file_path()
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_path, parser)
        root = tree.getroot()

        if root.xpath("//alumno[@id=$i]", i=str(datos["id"])):
            raise ValueError(
                f"El alumno con ID {datos['id']} ya existe."
            )

        nuevo_alumno = etree.Element(
            "alumno",
            id=datos["id"],
            matricula=datos["matricula"],
        )

        for campo in self.campos_esperados:
            hijo = etree.Element(campo)
            hijo.text = str(datos.get(campo, ""))
            nuevo_alumno.append(hijo)

        root.append(nuevo_alumno)
        self._guardar_xml(tree, xml_path)
        return datos

    def eliminar_alumno(self, alumno_id):
        xml_path = self._get_file_path()
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_path, parser)
        root = tree.getroot()

        nodos = root.xpath("//alumno[@id=$i]", i=alumno_id)

        if not nodos:
            return False

        root.remove(nodos[0])
        self._guardar_xml(tree, xml_path)
        return True

    # ==========================
    # Operaciones CRUD Materias
    # ==========================

    def listar_materias(self):
        """Retorna el catálogo de materias."""
        xml_path = self._get_file_path()

        if not os.path.exists(xml_path):
            return []

        tree = etree.parse(xml_path)
        materias = []

        for m in tree.xpath("//materia"):
            carrera_nodo = m.find("carrera")
            profesor_nodo = m.find("profesor")

            materias.append({
                "id": m.get("id"),
                "clave": m.get("clave"),
                "nombre": (m.findtext("nombre") or "").strip(),
                "descripcion": (
                    m.findtext("descripcion") or ""
                ).strip(),
                "creditos": int(
                    (m.findtext("creditos") or "0").strip()
                ),
                "semestre": int(
                    (m.findtext("semestre") or "0").strip()
                ),
                "carrera_codigo": (
                    carrera_nodo.get("codigo")
                    if carrera_nodo is not None else ""
                ),
                "carrera": (m.findtext("carrera") or "").strip(),
                "profesor_id": (
                    profesor_nodo.get("id")
                    if profesor_nodo is not None else ""
                ),
                "profesor": (m.findtext("profesor") or "").strip(),
                "prerrequisitos": [
                    {
                        "ref": p.get("ref"),
                        "nombre": p.get("nombre"),
                    }
                    for p in m.xpath(
                        "prerrequisitos/prerrequisito"
                    )
                ],
            })

        return materias

    def agregar_materia(self, datos):
        """Agrega una materia y valida el XML."""
        xml_path = self._get_file_path()
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_path, parser)
        root = tree.getroot()

        materia_id = str(datos.get("id", "")).strip().upper()
        clave = str(datos.get("clave", "")).strip().upper()

        if root.xpath("//materia[@id=$i]", i=materia_id):
            raise ValueError(
                f"La materia con ID '{materia_id}' ya existe."
            )

        nueva = etree.Element(
            "materia", id=materia_id, clave=clave
        )

        etree.SubElement(nueva, "nombre").text = str(
            datos.get("nombre", "")
        ).strip()
        etree.SubElement(nueva, "descripcion").text = str(
            datos.get("descripcion", "")
        ).strip()
        etree.SubElement(nueva, "creditos").text = str(
            datos.get("creditos", "6")
        ).strip()
        etree.SubElement(nueva, "semestre").text = str(
            datos.get("semestre", "1")
        ).strip()

        carrera_el = etree.SubElement(
            nueva,
            "carrera",
            codigo=str(
                datos.get("carrera_codigo", "ICC")
            ).strip().upper(),
        )
        carrera_el.text = str(
            datos.get(
                "carrera_nombre",
                "Ingeniería en Ciencias de la Computación",
            )
        ).strip()

        profesor_el = etree.SubElement(
            nueva,
            "profesor",
            id=str(datos.get("profesor_id", "P001"))
            .strip().upper(),
        )
        profesor_el.text = str(
            datos.get("profesor_nombre", "")
        ).strip()

        prerreq_el = etree.SubElement(nueva, "prerrequisitos")
        prerreqs = datos.get("prerrequisitos", [])

        if isinstance(prerreqs, str):
            prerreqs = [
                r.strip()
                for r in prerreqs.split(",")
                if r.strip()
            ]

        for ref_id in prerreqs:
            nodo_ref = root.xpath("//materia[@id=$i]", i=str(ref_id))
            nombre_ref = (
                nodo_ref[0].findtext("nombre") or ""
            ).strip() if nodo_ref else ref_id

            etree.SubElement(
                prerreq_el,
                "prerrequisito",
                ref=ref_id,
                nombre=nombre_ref,
            )

        root.append(nueva)
        self._guardar_xml(tree, xml_path)
        return datos

    def eliminar_materia(self, materia_id):
        """Evita eliminar materias con prerrequisitos dependientes."""
        xml_path = self._get_file_path()
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_path, parser)
        root = tree.getroot()

        dependientes = root.xpath(
            "//materia[prerrequisitos/prerrequisito[@ref=$i]]/@id",
            i=materia_id,
        )

        if dependientes:
            raise ValueError(
                f"No se puede eliminar {materia_id} porque "
                "es prerrequisito de: "
                f"{', '.join(dependientes)}"
            )

        nodos = root.xpath("//materia[@id=$i]", i=materia_id)

        if not nodos:
            return False

        root.remove(nodos[0])
        self._guardar_xml(tree, xml_path)
        return True

    # ==========================
    # Operaciones CRUD Profesores
    # ==========================

    def listar_profesores(self):
        """Retorna profesores y las materias que imparten."""
        xml_path = self._get_file_path()

        if not os.path.exists(xml_path):
            return []

        tree = etree.parse(xml_path)
        profesores = []

        for nodo in tree.getroot().findall("profesor"):
            profesor = {
                "id": nodo.get("id"),
                "nombre": nodo.findtext("nombre", default=""),
                "especialidad": nodo.findtext(
                    "especialidad", default=""
                ),
                "correo": nodo.findtext("correo", default=""),
                "departamento": nodo.findtext(
                    "departamento", default=""
                ),
                "materias_impartidas": [
                    {
                        "codigo": materia.get("codigo", ""),
                        "nombre": materia.text or "",
                    }
                    for materia in nodo.findall(
                        "materias_impartidas/materia"
                    )
                ],
            }
            profesores.append(profesor)

        return profesores

    def obtener_profesor(self, profesor_id):
        """Busca un profesor por su ID."""
        for profesor in self.listar_profesores():
            if profesor["id"] == profesor_id:
                return profesor

        return None

    def agregar_profesor(self, datos):
        """Registra un profesor y sus materias impartidas."""
        campos = [
            "id",
            "nombre",
            "especialidad",
            "correo",
            "departamento",
        ]

        for campo in campos:
            if (
                not isinstance(datos.get(campo), str)
                or not datos[campo].strip()
            ):
                raise ValueError(
                    f"El campo '{campo}' es obligatorio."
                )

        profesor_id = datos["id"].strip()
        materias = datos.get("materias_impartidas", [])

        if not isinstance(materias, list):
            raise ValueError(
                "'materias_impartidas' debe ser una lista."
            )

        for materia in materias:
            if not isinstance(materia, dict):
                raise ValueError(
                    "Cada materia debe ser un objeto."
                )

            codigo = materia.get("codigo")
            nombre = materia.get("nombre")

            if not isinstance(codigo, str) or not codigo.strip():
                raise ValueError(
                    "Cada materia debe tener un código válido."
                )

            if not isinstance(nombre, str) or not nombre.strip():
                raise ValueError(
                    "Cada materia debe tener un nombre."
                )

        xml_path = self._get_file_path()

        if not os.path.exists(xml_path):
            raise ValueError(
                "No existe profesores.xml. "
                "Verifica la ruta del catálogo."
            )

        tree = etree.parse(xml_path)
        root = tree.getroot()

        if any(
            p.get("id") == profesor_id
            for p in root.findall("profesor")
        ):
            raise ValueError(
                f"El profesor con ID {profesor_id} ya existe."
            )

        nuevo = etree.SubElement(
            root, "profesor", id=profesor_id
        )

        for campo in campos[1:]:
            hijo = etree.SubElement(nuevo, campo)
            hijo.text = datos[campo].strip()

        materias_xml = etree.SubElement(
            nuevo, "materias_impartidas"
        )

        for materia in materias:
            elemento = etree.SubElement(
                materias_xml,
                "materia",
                codigo=materia["codigo"].strip(),
            )
            elemento.text = materia["nombre"].strip()

        self._guardar_xml(tree, xml_path)
        return self.obtener_profesor(profesor_id)

    def actualizar_profesor(self, profesor_id, datos):
        """Actualiza un profesor existente."""
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
            None,
        )

        if nodo is None:
            return None

        campos = [
            "nombre",
            "especialidad",
            "correo",
            "departamento",
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
                    raise ValueError(
                        "Cada materia debe ser un objeto."
                    )

                codigo = materia.get("codigo")
                nombre = materia.get("nombre")

                if not isinstance(codigo, str) or not codigo.strip():
                    raise ValueError(
                        "Cada materia debe tener un código válido."
                    )

                if not isinstance(nombre, str) or not nombre.strip():
                    raise ValueError(
                        "Cada materia debe tener un nombre."
                    )

            materias_xml = nodo.find("materias_impartidas")

            if materias_xml is None:
                materias_xml = etree.SubElement(
                    nodo, "materias_impartidas"
                )

            for materia in list(materias_xml):
                materias_xml.remove(materia)

            for materia in materias:
                elemento = etree.SubElement(
                    materias_xml,
                    "materia",
                    codigo=materia["codigo"].strip(),
                )
                elemento.text = materia["nombre"].strip()

        self._guardar_xml(tree, xml_path)
        return self.obtener_profesor(profesor_id)

    def eliminar_profesor(self, profesor_id):
        """Elimina un profesor por su ID."""
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
            None,
        )

        if nodo is None:
            return False

        root.remove(nodo)
        self._guardar_xml(tree, xml_path)
        return True
