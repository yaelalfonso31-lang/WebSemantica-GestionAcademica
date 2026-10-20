"""Resolución de directorios: usa app.config si hay app activa y, si no, config.py."""
import os

from flask import current_app

import config


def directorio(clave):
    try:
        return current_app.config.get(clave, getattr(config, clave))
    except RuntimeError:  # fuera de contexto de aplicación (scripts, tests unitarios)
        return getattr(config, clave)


def ruta(clave, *partes):
    return os.path.join(directorio(clave), *partes)


def ajuste(clave):
    """Lee un ajuste escalar (CALIFICACION_MINIMA, PERIODO_ACTUAL, ...)."""
    return directorio(clave)
