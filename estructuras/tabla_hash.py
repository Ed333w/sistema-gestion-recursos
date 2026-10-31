"""
TABLA HASH — Estructura de datos propia

Descripción:
    Tabla hash con encadenamiento por colisiones (sin usar list nativa).
    Usado en M02 para búsqueda O(1) de recursos por código.

Implementación:
    - Tabla de tamaño fijo con arreglo de cadenas (listas enlazadas)
    - Cada celda contiene una lista enlazada de pares (clave, valor)
    - Función hash: suma ASCII módulo tamaño

Complejidad:
    - Caso promedio: O(1) insertar, buscar, eliminar
    - Peor caso: O(n) si todas las claves colisionan
"""


class _Nodo:
    """Nodo para lista enlazada en cadena de colisiones."""
    def __init__(self, clave, valor):
        self.clave = clave
        self.valor = valor
        self.siguiente = None


class TablaHash:
    """
    Tabla hash con encadenamiento.

    Atributos:
        tabla (arreglo): Arreglo de cabeceras de listas enlazadas
        tamaño (int): Cantidad de celdas
        cantidad (int): Cantidad total de pares clave-valor

    Métodos principales:
        insertar(clave, valor): Agregar/actualizar
        buscar(clave): Obtener valor
        eliminar(clave): Quitar elemento
        contiene(clave): ¿Existe?
    """

    def __init__(self, tamaño=100):
        """Inicializa tabla hash."""
        self.tamaño = tamaño
        self.tabla = [None] * tamaño  # Arreglo de cabeceras
        self.cantidad = 0

    def _hash(self, clave):
        """
        Calcula función hash.

        Returns:
            Índice en tabla (0 a tamaño-1)

        Complejidad: O(len(clave)) para strings
        """
        if isinstance(clave, str):
            # Suma ASCII de caracteres módulo tamaño
            h = 0
            for c in clave:
                h += ord(c)
            return h % self.tamaño
        else:
            # Para números, usar módulo directo
            return abs(hash(clave)) % self.tamaño

    def insertar(self, clave, valor):
        """
        Inserta o actualiza un par clave-valor.

        Complejidad: O(1) promedio, O(n) peor caso
        """
        idx = self._hash(clave)

        # Buscar si ya existe en la cadena
        nodo = self.tabla[idx]
        while nodo is not None:
            if nodo.clave == clave:
                nodo.valor = valor  # Actualizar
                return
            nodo = nodo.siguiente

        # No existe, agregar al inicio de la cadena
        nuevo_nodo = _Nodo(clave, valor)
        nuevo_nodo.siguiente = self.tabla[idx]
        self.tabla[idx] = nuevo_nodo
        self.cantidad += 1

    def buscar(self, clave):
        """
        Busca el valor asociado a una clave.

        Returns:
            El valor, o None si no existe

        Complejidad: O(1) promedio, O(n) peor caso
        """
        idx = self._hash(clave)

        nodo = self.tabla[idx]
        while nodo is not None:
            if nodo.clave == clave:
                return nodo.valor
            nodo = nodo.siguiente

        return None

    def eliminar(self, clave):
        """
        Elimina un par clave-valor.

        Returns:
            True si se eliminó, False si no existía

        Complejidad: O(1) promedio, O(n) peor caso
        """
        idx = self._hash(clave)

        # Caso 1: Eliminar del inicio de la cadena
        if self.tabla[idx] is not None and self.tabla[idx].clave == clave:
            self.tabla[idx] = self.tabla[idx].siguiente
            self.cantidad -= 1
            return True

        # Caso 2: Buscar en el resto de la cadena
        nodo = self.tabla[idx]
        while nodo is not None and nodo.siguiente is not None:
            if nodo.siguiente.clave == clave:
                nodo.siguiente = nodo.siguiente.siguiente
                self.cantidad -= 1
                return True
            nodo = nodo.siguiente

        return False

    def contiene(self, clave):
        """
        Verifica si una clave existe.

        Returns:
            True si existe, False en otro caso

        Complejidad: O(1) promedio, O(n) peor caso
        """
        return self.buscar(clave) is not None

    def obtener_cantidad(self):
        """Retorna cantidad de pares. O(1)."""
        return self.cantidad

    def obtener_factor_carga(self):
        """
        Retorna factor de carga (cantidad / tamaño).
        Indicador de qué tan llena está la tabla.

        Complejidad: O(1)
        """
        return self.cantidad / self.tamaño if self.tamaño > 0 else 0

    def obtener_todas_las_claves(self):
        """
        Retorna lista de todas las claves.

        Complejidad: O(n)
        """
        claves = []
        for celda in self.tabla:
            nodo = celda
            while nodo is not None:
                claves.append(nodo.clave)
                nodo = nodo.siguiente
        return claves

    def limpiar(self):
        """Vacía la tabla. O(1)."""
        self.tabla = [None] * self.tamaño
        self.cantidad = 0

    def __str__(self):
        """Representación en string."""
        return f"TablaHash(cantidad={self.cantidad}, tamaño={self.tamaño}, factor_carga={self.obtener_factor_carga():.2f})"

    def __repr__(self):
        """Representación para debug."""
        return self.__str__()
