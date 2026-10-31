"""Clase Prestamo — M03"""
from datetime import datetime

class Prestamo:
    """Representa un préstamo de recurso."""

    def __init__(self, codigo, usuario_codigo, recurso_codigo, sede, fecha_prestamo=None, dias_limite=14):
        self.codigo = codigo
        self.usuario_codigo = usuario_codigo
        self.recurso_codigo = recurso_codigo
        self.sede = sede
        self.fecha_prestamo = fecha_prestamo if fecha_prestamo else datetime.now()
        self.dias_limite = dias_limite
        self.fecha_devolucion = None
        self.estado = "Activo"  # Activo, Devuelto, Atrasado

    def devolver(self):
        """Registra devolución."""
        self.fecha_devolucion = datetime.now()
        self.estado = "Devuelto"

    def reactivar(self):
        """Revierte una devolución (usado por deshacer)."""
        self.fecha_devolucion = None
        self.estado = "Activo"

    def dias_atraso(self, ahora=None):
        """Días de atraso (0 si no está activo o está a tiempo)."""
        if self.estado != "Activo":
            return 0
        ahora = ahora if ahora else datetime.now()
        return max(0, (ahora - self.fecha_prestamo).days - self.dias_limite)

    def esta_atrasado(self, ahora=None):
        """Verifica si está atrasado."""
        return self.dias_atraso(ahora) > 0

    def obtener_info(self):
        return {
            'codigo': self.codigo,
            'usuario': self.usuario_codigo,
            'recurso': self.recurso_codigo,
            'sede': self.sede,
            'fecha_prestamo': self.fecha_prestamo.strftime("%Y-%m-%d %H:%M"),
            'estado': self.estado,
            'atrasado': self.esta_atrasado(),
        }

    def __str__(self):
        return f"Prestamo({self.codigo}: {self.usuario_codigo} ← {self.recurso_codigo}, {self.estado})"
