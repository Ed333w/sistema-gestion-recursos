"""
LISTA ENLAZADA SIMPLE — Estructura de datos propia

Descripción:
    Estructura basada en nodos, donde cada nodo apunta al siguiente.
    Usado en M03 para historial de préstamos (navegación hacia adelante).

Ventajas vs Vector:
    - Inserción/eliminación O(1) si tienes el nodo (vs O(n) en vector)
    - No necesita redimensionamiento
    - Crecimiento sin límite sin costo de copia

Desventajas vs Vector:
    - Acceso O(n) (vs O(1) en vector)
    - Requiere más memoria (apuntador siguiente)

Funcionalidad:
    - Agregar al final: O(n) (debe buscar el último)
    - Agregar al inicio: O(1)
    - Buscar: O(n)
    - Eliminar: O(n)
    - Recorrer: O(n)

Requerimientos que resuelve:
    - M03: Historial de préstamos navegable (hacia adelante)
          "¿Cuáles fueron mis últimos 5 préstamos?"
"""


class NodoSimple:
    """
    Nodo para lista enlazada simple.

    Atributos:
        dato: El valor almacenado
        siguiente: Referencia al siguiente nodo (None si es último)
    """

    def __init__(self, dato):
        """
        Crea un nodo con un dato.

        Args:
            dato: Valor a almacenar
        """
        self.dato = dato
        self.siguiente = None

    def __str__(self):
        return f"NodoSimple({self.dato})"


class ListaSimple:
    """
    Lista enlazada simple.

    Atributos:
        cabeza (NodoSimple): Primer nodo de la lista
        tamaño (int): Cantidad de nodos

    Métodos principales:
        agregar_al_inicio(dato): Insertar al principio
        agregar_al_final(dato): Insertar al final
        eliminar_inicio(): Quitar el primer nodo
        buscar(criterio_fn): Buscar nodo que cumpla criterio
        recorrer(): Obtener lista de datos
        obtener_tamaño(): Cantidad de nodos

    Ejemplo de uso en M03 (Préstamos):
        >>> historial = ListaSimple()
        >>> historial.agregar_al_final(prestamo1)
        >>> historial.agregar_al_final(prestamo2)
        >>> for prestamo in historial.recorrer():
        ...     print(prestamo)  # Ver histórico en orden
    """

    def __init__(self):
        """Inicializa lista vacía."""
        self.cabeza = None
        self.tamaño = 0

    def agregar_al_inicio(self, dato):
        """
        Agrega elemento al inicio de la lista.

        Args:
            dato: Elemento a agregar

        Complejidad: O(1)

        Ejemplo:
            >>> lista = ListaSimple()
            >>> lista.agregar_al_inicio("A")
            >>> lista.agregar_al_inicio("B")
            >>> lista.recorrer()
            ['B', 'A']
        """
        nuevo_nodo = NodoSimple(dato)
        nuevo_nodo.siguiente = self.cabeza
        self.cabeza = nuevo_nodo
        self.tamaño += 1

    def agregar_al_final(self, dato):
        """
        Agrega elemento al final de la lista.

        Args:
            dato: Elemento a agregar

        Complejidad: O(n) porque debe buscar el último

        Ejemplo:
            >>> lista = ListaSimple()
            >>> lista.agregar_al_final("A")
            >>> lista.agregar_al_final("B")
            >>> lista.recorrer()
            ['A', 'B']

        Nota: En M03, se usa para historial de préstamos,
              donde queremos el orden cronológico.
        """
        nuevo_nodo = NodoSimple(dato)

        if self.cabeza is None:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

        self.tamaño += 1

    def eliminar_inicio(self):
        """
        Elimina el primer nodo.

        Returns:
            El dato del nodo eliminado, o None si lista vacía

        Complejidad: O(1)

        Ejemplo:
            >>> lista = ListaSimple()
            >>> lista.agregar_al_final("A")
            >>> lista.agregar_al_final("B")
            >>> lista.eliminar_inicio()
            'A'
            >>> lista.recorrer()
            ['B']
        """
        if self.cabeza is None:
            return None

        dato = self.cabeza.dato
        self.cabeza = self.cabeza.siguiente
        self.tamaño -= 1
        return dato

    def buscar(self, criterio_fn):
        """
        Busca el primer nodo que cumpla un criterio.

        Args:
            criterio_fn: Función que toma un dato y retorna True/False

        Returns:
            El dato encontrado, o None

        Complejidad: O(n)

        Ejemplo en M03 (Préstamos):
            >>> historial = ListaSimple()
            >>> historial.agregar_al_final(prestamo1)  # código='P001'
            >>> historial.agregar_al_final(prestamo2)  # código='P002'
            >>> prestamo = historial.buscar(lambda p: p.codigo == 'P001')
            >>> print(prestamo.codigo)
            'P001'
        """
        actual = self.cabeza
        while actual is not None:
            if criterio_fn(actual.dato):
                return actual.dato
            actual = actual.siguiente
        return None

    def recorrer(self):
        """
        Obtiene lista de todos los datos en orden.

        Returns:
            Lista con los datos (copia)

        Complejidad: O(n)

        Ejemplo:
            >>> lista = ListaSimple()
            >>> lista.agregar_al_final("A")
            >>> lista.agregar_al_final("B")
            >>> lista.recorrer()
            ['A', 'B']
        """
        resultado = []
        actual = self.cabeza
        while actual is not None:
            resultado.append(actual.dato)
            actual = actual.siguiente
        return resultado

    def obtener_tamaño(self):
        """
        Obtiene cantidad de nodos.

        Returns:
            int: Cantidad de nodos

        Complejidad: O(1)
        """
        return self.tamaño

    def esta_vacia(self):
        """
        Verifica si la lista está vacía.

        Returns:
            True si tamaño == 0

        Complejidad: O(1)
        """
        return self.tamaño == 0

    def limpiar(self):
        """
        Vacía la lista.

        Complejidad: O(1)
        """
        self.cabeza = None
        self.tamaño = 0

    def __str__(self):
        """Representación en string."""
        return f"ListaSimple({self.recorrer()})"

    def __repr__(self):
        """Representación para debug."""
        return self.__str__()
