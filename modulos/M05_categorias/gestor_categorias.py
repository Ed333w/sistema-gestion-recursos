"""Gestor de Categorías — CLASE PRINCIPAL DE M05"""

from estructuras import ArbolBinario, TablaHash


class Categoria:
    """Entidad Categoría con código y nombre."""

    def __init__(self, codigo, nombre):
        """
        Inicializa una categoría.

        Args:
            codigo: str (C001, C002, etc.)
            nombre: str (nombre de la categoría)
        """
        self.codigo = codigo
        self.nombre = nombre

    def __str__(self):
        return f"Categoria({self.codigo}: {self.nombre})"

    def __repr__(self):
        return self.__str__()


class GestorCategorias:
    """
    Gestiona categorías usando árbol binario.

    CLASE PRINCIPAL DE M05.
    """

    def __init__(self):
        """Inicializa gestor de categorías."""
        self.arbol = ArbolBinario()
        # Antes era un dict de Python; el curso exige estructuras propias y
        # la TablaHash permite comprobar en O(1) promedio si un código ya existe.
        self.categorias = TablaHash(211)  # código -> Categoria

    def registrar_categoria(self, codigo, nombre):
        """
        Registra una nueva categoría.

        Args:
            codigo: str
            nombre: str

        Returns:
            str: código de la categoría

        Raises:
            ValueError: si el código ya está registrado (RF7: sin repetidos)

        Complejidad: O(log n) promedio
        """
        # Sin esta validación, insertar() de la TablaHash actualiza el valor y la
        # segunda categoría C1 sobrescribía el nombre de la primera.
        if self.categorias.contiene(codigo):
            raise ValueError(f"La categoria {codigo} ya existe")
        cat = Categoria(codigo, nombre)
        self.categorias.insertar(codigo, cat)
        # Insertar en árbol con criterio de comparación lexicográfica
        self.arbol.insertar(codigo, lambda nuevo, existente: -1 if nuevo < existente else (1 if nuevo > existente else 0))
        return codigo

    def obtener_categoria(self, codigo):
        """
        Obtiene categoría por código.

        Args:
            codigo: str

        Returns:
            Categoria o None

        Complejidad: O(1) promedio
        """
        return self.categorias.buscar(codigo)

    def obtener_cantidad(self):
        """Obtiene cantidad de categorías registradas."""
        return self.categorias.obtener_cantidad()
