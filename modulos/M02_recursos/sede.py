"""Entidad Sede — Ubicación de recursos"""


class Sede:
    """Entidad Sede con código y nombre."""

    def __init__(self, codigo, nombre):
        """
        Inicializa una sede.

        Args:
            codigo: str (S001, S002, etc.)
            nombre: str (nombre de la sede)
        """
        self.codigo = codigo
        self.nombre = nombre
        self.conectada = True

    def __str__(self):
        return f"Sede({self.codigo}: {self.nombre})"

    def __repr__(self):
        return self.__str__()
