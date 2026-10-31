"""Clase Solicitud — M04"""
from datetime import datetime


class Solicitud:
    """Representa una solicitud de turno para un recurso."""

    def __init__(self, codigo, usuario_codigo, recurso_codigo, fecha=None):
        self.codigo = codigo
        self.usuario_codigo = usuario_codigo
        self.recurso_codigo = recurso_codigo
        self.fecha = fecha if fecha else datetime.now()
        self.estado = "En espera"  # En espera | Otorgado | Cancelado

    def otorgar(self):
        """Cambia estado a Otorgado."""
        self.estado = "Otorgado"

    def cancelar(self):
        """Cambia estado a Cancelado."""
        self.estado = "Cancelado"

    def reiniciar(self):
        """Vuelve la solicitud a En espera."""
        self.estado = "En espera"

    def __str__(self):
        return f"Solicitud({self.codigo}: {self.usuario_codigo}, {self.estado})"
