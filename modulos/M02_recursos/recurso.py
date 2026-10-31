"""
Clase Recurso (Base) — M02

Clase abstracta que define la interfaz común para todos los recursos.

Atributos comunes:
    - código: Identificador único
    - nombre: Nombre del recurso
    - fecha_registro: Cuándo se registró
    - estado: Disponible/No disponible/Dado de baja
    - cantidad_prestamos: Historial de usos

Métodos que heredan:
    - obtener_info(): Información básica
    - es_disponible(): ¿Está disponible?
    - registrar_prestamo(): Contar un uso
    - dar_de_baja(): Desactivar

Las subclases (Libro, Equipo, Sala) heredan estos y agregan atributos específicos.
"""

from datetime import datetime
from abc import ABC, abstractmethod


class Recurso(ABC):
    """
    Clase base abstracta para todos los recursos.

    Atributos:
        codigo (str): Identificador único
        nombre (str): Nombre del recurso
        fecha_registro (datetime): Cuándo se registró
        estado (str): "Disponible", "No disponible", "Dado de baja"
        cantidad_prestamos (int): Cuántas veces se ha prestado

    Métodos:
        obtener_info(): Información del recurso
        es_disponible(): ¿Se puede prestar?
        registrar_prestamo(): Contar un uso
        dar_de_baja(): Desactivar
        __str__: Representación

    Nota:
        Esta es una clase ABSTRACTA (base).
        No se instancia directamente.
        Se usan las subclases: Libro, Equipo, Sala.
    """

    def __init__(self, codigo, nombre):
        """
        Constructor de la clase base.

        Args:
            codigo (str): Identificador único
            nombre (str): Nombre del recurso
        """
        self.codigo = codigo
        self.nombre = nombre
        self.fecha_registro = datetime.now()
        self.estado = "Disponible"
        self.cantidad_prestamos = 0

    @abstractmethod
    def obtener_tipo(self):
        """
        Retorna el tipo de recurso.

        Debe ser implementado por las subclases.

        Returns:
            str: "Libro", "Equipo" o "Sala"
        """
        pass

    @abstractmethod
    def obtener_info(self):
        """
        Retorna información detallada del recurso.

        Debe ser implementado por las subclases
        para incluir sus atributos específicos.

        Returns:
            dict: Información del recurso
        """
        pass

    def es_disponible(self):
        """
        Verifica si el recurso está disponible para préstamo.

        Returns:
            bool: True si estado == "Disponible"

        Ejemplo:
            >>> libro = Libro("R001", "Python", "Guido", "978-123")
            >>> libro.es_disponible()
            True
            >>> libro.marcar_no_disponible()
            >>> libro.es_disponible()
            False
        """
        return self.estado == "Disponible"

    def marcar_no_disponible(self):
        """
        Marca el recurso como no disponible.
        Ej: está siendo reparado, en proceso de préstamo, etc.
        """
        self.estado = "No disponible"

    def marcar_disponible(self):
        """
        Marca el recurso como disponible.
        """
        self.estado = "Disponible"

    def registrar_prestamo(self):
        """
        Registra que este recurso fue prestado.
        Incrementa el contador de usos.

        Ejemplo:
            >>> libro = Libro("R001", "Python", "Guido", "978-123")
            >>> libro.cantidad_prestamos
            0
            >>> libro.registrar_prestamo()
            >>> libro.cantidad_prestamos
            1
        """
        self.cantidad_prestamos += 1

    def dar_de_baja(self):
        """
        Marca el recurso como dado de baja.
        Ya no se puede prestar.

        Ejemplo:
            >>> libro = Libro("R001", "Python", "Guido", "978-123")
            >>> libro.dar_de_baja()
            >>> libro.estado
            'Dado de baja'
        """
        self.estado = "Dado de baja"

    def reactivar(self):
        """
        Reactiva un recurso que estaba dado de baja.
        """
        self.estado = "Disponible"

    def obtener_estado(self):
        """Retorna el estado actual."""
        return self.estado

    def obtener_cantidad_prestamos(self):
        """Retorna cuántas veces se ha prestado."""
        return self.cantidad_prestamos

    def __str__(self):
        """Representación legible."""
        return f"{self.obtener_tipo()}({self.codigo}: {self.nombre}, {self.estado})"

    def __repr__(self):
        """Para debug."""
        return f"{self.__class__.__name__}(codigo='{self.codigo}', nombre='{self.nombre}', estado='{self.estado}', prestamos={self.cantidad_prestamos})"

    def __eq__(self, otro):
        """Comparación por código."""
        if isinstance(otro, Recurso):
            return self.codigo == otro.codigo
        return False
