"""
Clase Equipo — M02 (HERENCIA)

Representa un equipo (computador, proyector, etc.) en el sistema.
Hereda de Recurso y agrega atributos específicos de equipos.

Atributos propios:
    - tipo_equipo: Tipo específico (Computador, Proyector, etc.)
    - modelo: Modelo del equipo
    - ubicacion: Dónde se encuentra normalmente
"""

from .recurso import Recurso


class Equipo(Recurso):
    """
    Representa un equipo en la biblioteca.

    Hereda de Recurso todos los métodos comunes.
    Agrega atributos específicos de equipos.

    Atributos:
        codigo (str): Identificador único (heredado)
        nombre (str): Nombre del equipo (heredado)
        tipo_equipo (str): Tipo (Computador, Proyector, etc.) (NUEVO)
        modelo (str): Modelo del equipo (NUEVO)
        ubicacion (str): Ubicación física (NUEVO)
        estado (str): "Disponible"/"No disponible"/"Dado de baja" (heredado)
        cantidad_prestamos (int): Cuántas veces se prestó (heredado)

    Ejemplo de uso:
        >>> equipo = Equipo("E001", "Proyector Epson", "Proyector", "EB-S41", "Sala A")
        >>> print(equipo.obtener_tipo())
        'Equipo'
        >>> print(equipo.tipo_equipo)
        'Proyector'
        >>> print(equipo.modelo)
        'EB-S41'
        >>> equipo.registrar_prestamo()
        >>> print(equipo.cantidad_prestamos)
        1
    """

    def __init__(self, codigo, nombre, tipo_equipo, modelo, ubicacion):
        """
        Crea un equipo.

        Args:
            codigo (str): Identificador único
            nombre (str): Nombre del equipo
            tipo_equipo (str): Tipo (Computador, Proyector, Impresora, etc.)
            modelo (str): Modelo específico
            ubicacion (str): Ubicación donde se guarda normalmente

        Ejemplo:
            >>> equipo = Equipo("E001", "PC Principal", "Computador", "Dell XPS 15", "Cubículo 1")
            >>> print(equipo.codigo)
            'E001'
        """
        super().__init__(codigo, nombre)
        self.tipo_equipo = tipo_equipo
        self.modelo = modelo
        self.ubicacion = ubicacion

    def obtener_tipo(self):
        """
        Retorna el tipo de recurso.

        Returns:
            str: "Equipo"
        """
        return "Equipo"

    def obtener_info(self):
        """
        Retorna información completa del equipo.

        Returns:
            dict: Información del equipo
        """
        return {
            'codigo': self.codigo,
            'tipo': self.obtener_tipo(),
            'nombre': self.nombre,
            'tipo_equipo': self.tipo_equipo,
            'modelo': self.modelo,
            'ubicacion': self.ubicacion,
            'estado': self.estado,
            'cantidad_prestamos': self.cantidad_prestamos,
            'fecha_registro': self.fecha_registro.strftime("%Y-%m-%d"),
            'disponible': self.es_disponible(),
        }

    def obtener_tipo_equipo(self):
        """Obtiene el tipo de equipo."""
        return self.tipo_equipo

    def obtener_modelo(self):
        """Obtiene el modelo."""
        return self.modelo

    def obtener_ubicacion(self):
        """Obtiene la ubicación."""
        return self.ubicacion

    def cambiar_ubicacion(self, nueva_ubicacion):
        """Cambia la ubicación del equipo."""
        self.ubicacion = nueva_ubicacion

    def __str__(self):
        """Representación legible."""
        return f"Equipo({self.codigo}: {self.nombre} ({self.tipo_equipo} {self.modelo}), {self.estado}, en {self.ubicacion})"

    def __repr__(self):
        """Para debug."""
        return f"Equipo(codigo='{self.codigo}', nombre='{self.nombre}', tipo='{self.tipo_equipo}', modelo='{self.modelo}')"
