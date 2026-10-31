"""
Clase Sala — M02 (HERENCIA)

Representa una sala de estudio en el sistema.
Hereda de Recurso y agrega atributos específicos de salas.

Atributos propios:
    - capacidad: Cuántas personas caben
    - recursos_disponibles: Lista de recursos en la sala (mesas, sillas, etc.)
"""

from .recurso import Recurso


class Sala(Recurso):
    """
    Representa una sala de estudio en la biblioteca.

    Hereda de Recurso todos los métodos comunes.
    Agrega atributos específicos de salas.

    Atributos:
        codigo (str): Identificador único (heredado)
        nombre (str): Nombre de la sala (heredado)
        capacidad (int): Capacidad máxima de personas (NUEVO)
        recursos_disponibles (list): Muebles/recursos en la sala (NUEVO)
        estado (str): "Disponible"/"No disponible"/"Dado de baja" (heredado)
        cantidad_prestamos (int): Cuántas veces se reservó (heredado)

    Ejemplo de uso:
        >>> sala = Sala("S001", "Sala A", 30, ["Mesas", "Sillas", "Pizarras"])
        >>> print(sala.obtener_tipo())
        'Sala'
        >>> print(sala.capacidad)
        30
        >>> print(sala.es_disponible())
        True
        >>> sala.registrar_prestamo()  # Alguien la reservó
        >>> print(sala.cantidad_prestamos)
        1
    """

    def __init__(self, codigo, nombre, capacidad, recursos_disponibles=None):
        """
        Crea una sala.

        Args:
            codigo (str): Identificador único
            nombre (str): Nombre de la sala
            capacidad (int): Capacidad máxima
            recursos_disponibles (list): Recursos en la sala (default: lista vacía)

        Ejemplo:
            >>> sala = Sala("S001", "Sala de Estudio", 25, ["Mesas", "Sillas"])
            >>> print(sala.codigo)
            'S001'
            >>> print(sala.capacidad)
            25
        """
        super().__init__(codigo, nombre)
        self.capacidad = capacidad
        self.recursos_disponibles = recursos_disponibles if recursos_disponibles else []

    def obtener_tipo(self):
        """
        Retorna el tipo de recurso.

        Returns:
            str: "Sala"
        """
        return "Sala"

    def obtener_info(self):
        """
        Retorna información completa de la sala.

        Returns:
            dict: Información de la sala
        """
        return {
            'codigo': self.codigo,
            'tipo': self.obtener_tipo(),
            'nombre': self.nombre,
            'capacidad': self.capacidad,
            'recursos': self.recursos_disponibles.copy(),
            'estado': self.estado,
            'cantidad_reservas': self.cantidad_prestamos,  # "Préstamos" = reservas en salas
            'fecha_registro': self.fecha_registro.strftime("%Y-%m-%d"),
            'disponible': self.es_disponible(),
        }

    def obtener_capacidad(self):
        """Obtiene la capacidad máxima."""
        return self.capacidad

    def obtener_recursos(self):
        """Obtiene lista de recursos disponibles."""
        return self.recursos_disponibles.copy()

    def agregar_recurso(self, recurso):
        """
        Agrega un recurso a la sala.

        Args:
            recurso (str): Nombre del recurso
        """
        if recurso not in self.recursos_disponibles:
            self.recursos_disponibles.append(recurso)

    def remover_recurso(self, recurso):
        """
        Quita un recurso de la sala.

        Args:
            recurso (str): Nombre del recurso
        """
        if recurso in self.recursos_disponibles:
            self.recursos_disponibles.remove(recurso)

    def tiene_recurso(self, recurso):
        """
        Verifica si la sala tiene un recurso.

        Args:
            recurso (str): Nombre del recurso

        Returns:
            bool: True si lo tiene
        """
        return recurso in self.recursos_disponibles

    def __str__(self):
        """Representación legible."""
        return f"Sala({self.codigo}: {self.nombre}, capacidad={self.capacidad}, recursos={len(self.recursos_disponibles)}, {self.estado})"

    def __repr__(self):
        """Para debug."""
        return f"Sala(codigo='{self.codigo}', nombre='{self.nombre}', capacidad={self.capacidad})"
