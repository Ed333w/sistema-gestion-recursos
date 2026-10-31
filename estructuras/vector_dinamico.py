"""
VECTOR DINÁMICO — Estructura de datos propia

Descripción:
    Arreglo que crece automáticamente cuando se llena.
    Usado en M01 (usuarios) y M02 (recursos).

Funcionalidad:
    - Agregar elemento al final: O(1) amortizado
    - Acceder por índice: O(1)
    - Buscar: O(n)
    - Eliminar: O(n) en el peor caso
    - Recorrer: O(n)

Requerimientos que resuelve:
    - M01: Administrar padrón de usuarios sin límite previo
    - M02: Administrar catálogo de recursos sin límite previo

Diferencia con lista enlazada:
    - Vector: acceso O(1) por índice, inserción O(n)
    - Lista: acceso O(n), inserción O(1) si tienes el nodo

Estrategia de crecimiento:
    Cuando el vector se llena (tamaño == capacidad),
    duplicamos la capacidad y copiamos todos los elementos.
    Esto da O(1) amortizado para agregar.
"""


class VectorDinamico:
    """
    Vector dinámico que crece automáticamente.

    Atributos:
        datos (list): Arreglo Python (usado como contenedor de bajo nivel)
        tamaño (int): Cantidad actual de elementos
        capacidad (int): Capacidad actual del arreglo

    Métodos principales:
        agregar(elemento): Agregar al final
        eliminar_por_indice(indice): Eliminar por posición
        obtener(indice): Acceder a elemento
        buscar(elemento): Encontrar elemento
        recorrer(): Obtener lista de elementos
        esta_vacio(): Verificar si hay elementos
        obtener_tamaño(): Cantidad de elementos
    """

    def __init__(self, capacidad_inicial=10):
        """
        Inicializa el vector con capacidad inicial.

        Args:
            capacidad_inicial (int): Capacidad inicial del vector (default: 10)

        Ejemplo:
            >>> vector = VectorDinamico(5)
            >>> vector.agregar("Usuario1")
            >>> vector.obtener_tamaño()
            1
        """
        self.datos = [None] * capacidad_inicial
        self.tamaño = 0
        self.capacidad = capacidad_inicial

    def agregar(self, elemento):
        """
        Agrega un elemento al final del vector.
        Si está lleno, dobla la capacidad.

        Args:
            elemento: Elemento a agregar (cualquier tipo)

        Complejidad: O(1) amortizado

        Ejemplo:
            >>> vector = VectorDinamico(2)
            >>> vector.agregar("A")
            >>> vector.agregar("B")
            >>> vector.agregar("C")  # Se redimensiona aquí
            >>> vector.obtener_tamaño()
            3
        """
        if self.tamaño == self.capacidad:
            self._redimensionar()

        self.datos[self.tamaño] = elemento
        self.tamaño += 1

    def _redimensionar(self):
        """
        Dobla la capacidad del vector cuando se llena.

        Esto sucede automáticamente en agregar().

        Complejidad: O(n) pero sucede logarítmicamente pocas veces
        """
        nueva_capacidad = self.capacidad * 2
        nuevos_datos = [None] * nueva_capacidad

        for i in range(self.tamaño):
            nuevos_datos[i] = self.datos[i]

        self.datos = nuevos_datos
        self.capacidad = nueva_capacidad

    def obtener(self, indice):
        """
        Accede a un elemento por su índice.

        Args:
            indice (int): Posición (0-indexado)

        Returns:
            Elemento en esa posición, o None si índice inválido

        Complejidad: O(1)

        Ejemplo:
            >>> vector = VectorDinamico()
            >>> vector.agregar("Usuario1")
            >>> vector.obtener(0)
            'Usuario1'
        """
        if 0 <= indice < self.tamaño:
            return self.datos[indice]
        return None

    def eliminar_por_indice(self, indice):
        """
        Elimina elemento en una posición.
        Los elementos posteriores se desplazan hacia atrás.

        Args:
            indice (int): Posición a eliminar

        Returns:
            True si se eliminó, False si índice inválido

        Complejidad: O(n) en el peor caso

        Ejemplo:
            >>> vector = VectorDinamico()
            >>> vector.agregar("A")
            >>> vector.agregar("B")
            >>> vector.agregar("C")
            >>> vector.eliminar_por_indice(1)
            True
            >>> vector.obtener(1)
            'C'
        """
        if not (0 <= indice < self.tamaño):
            return False

        for i in range(indice, self.tamaño - 1):
            self.datos[i] = self.datos[i + 1]

        self.datos[self.tamaño - 1] = None
        self.tamaño -= 1
        return True

    def buscar(self, elemento):
        """
        Busca un elemento en el vector.

        Args:
            elemento: El elemento a buscar

        Returns:
            Índice del elemento, o -1 si no existe

        Complejidad: O(n)

        Ejemplo:
            >>> vector = VectorDinamico()
            >>> vector.agregar("Usuario1")
            >>> vector.agregar("Usuario2")
            >>> vector.buscar("Usuario1")
            0
            >>> vector.buscar("Usuario3")
            -1
        """
        for i in range(self.tamaño):
            if self.datos[i] == elemento:
                return i
        return -1

    def recorrer(self):
        """
        Obtiene lista de todos los elementos.

        Returns:
            Lista con los elementos (copia)

        Complejidad: O(n)

        Ejemplo:
            >>> vector = VectorDinamico()
            >>> vector.agregar("A")
            >>> vector.agregar("B")
            >>> vector.recorrer()
            ['A', 'B']
        """
        resultado = []
        for i in range(self.tamaño):
            resultado.append(self.datos[i])
        return resultado

    def esta_vacio(self):
        """
        Verifica si el vector está vacío.

        Returns:
            True si tamaño == 0

        Complejidad: O(1)
        """
        return self.tamaño == 0

    def obtener_tamaño(self):
        """
        Obtiene cantidad actual de elementos.

        Returns:
            int: Cantidad de elementos

        Complejidad: O(1)
        """
        return self.tamaño

    def obtener_capacidad(self):
        """
        Obtiene capacidad actual (para debug).

        Returns:
            int: Capacidad del arreglo

        Complejidad: O(1)
        """
        return self.capacidad

    def limpiar(self):
        """
        Vacía el vector (reseta a capacidad inicial).

        Complejidad: O(1)
        """
        self.datos = [None] * 10
        self.tamaño = 0
        self.capacidad = 10

    def __str__(self):
        """Representación en string."""
        return f"VectorDinamico({self.recorrer()}, tamaño={self.tamaño}, capacidad={self.capacidad})"

    def __repr__(self):
        """Representación para debug."""
        return self.__str__()
