"""
ÁRBOL BINARIO BÁSICO — Estructura de datos propia (Entrega 2)

Descripción:
    Árbol binario simple sin balanceo (NO es AVL).
    Usado en M07 para organizar categorías.

Funcionalidad:
    - insertar(dato, criterio): Agregar nodo
    - buscar(criterio): Encontrar nodo
    - recorrido_inorden(): Recorrido sorted
    - recorrido_preorden(): Recorrido top-down
    - recorrido_postorden(): Recorrido bottom-up

Complejidad:
    - Mejor/Promedio: O(log n)
    - Peor caso: O(n) si se vuelve degenerado (lista)

Aplicación en M07 (Categorías):
    Organizar categorías jerarquicamente:

                    Libros
                   /      \
              Ficción    No-ficción
              /    \        /      \
         Novela Romance  Historia Técnica

    Recorrido inorden: [Novela, Romance, Ficción, Historia, Técnica, No-ficción, Libros]
"""


class NodoArbol:
    """Nodo de árbol binario."""

    def __init__(self, dato):
        self.dato = dato
        self.izquierda = None
        self.derecha = None


class ArbolBinario:
    """
    Árbol binario simple.

    Atributos:
        raiz (NodoArbol): Nodo raíz
        tamaño (int): Cantidad de nodos

    Métodos:
        insertar(dato, criterio_comparar): Agregar nodo
        buscar(criterio): Encontrar nodo
        recorrido_inorden(): Lista en orden
        recorrido_preorden(): Recorrido raíz-primero
        recorrido_postorden(): Recorrido hoja-primero
        obtener_altura(): Altura del árbol
        obtener_cantidad(): Cantidad de nodos
    """

    def __init__(self):
        """Inicializa árbol vacío."""
        self.raiz = None
        self.tamaño = 0

    def insertar(self, dato, criterio_comparar):
        """
        Inserta un nodo en el árbol.

        Args:
            dato: El dato a insertar
            criterio_comparar: Función (dato_nuevo, dato_existente) -> -1, 0, 1
                              (-1: izquierda, 0: igual, 1: derecha)

        Complejidad: O(log n) promedio, O(n) peor caso

        Ejemplo en M07:
            >>> arbol = ArbolBinario()
            >>> def comparar(nuevo, existente):
            ...     return -1 if nuevo < existente else (1 if nuevo > existente else 0)
            >>> arbol.insertar("Novela", comparar)
            >>> arbol.insertar("Romance", comparar)
        """
        if self.raiz is None:
            self.raiz = NodoArbol(dato)
            self.tamaño = 1
        else:
            self._insertar_recursivo(self.raiz, dato, criterio_comparar)

    def _insertar_recursivo(self, nodo, dato, criterio):
        """Inserta recursivamente."""
        resultado = criterio(dato, nodo.dato)

        if resultado < 0:
            if nodo.izquierda is None:
                nodo.izquierda = NodoArbol(dato)
                self.tamaño += 1
            else:
                self._insertar_recursivo(nodo.izquierda, dato, criterio)
        elif resultado > 0:
            if nodo.derecha is None:
                nodo.derecha = NodoArbol(dato)
                self.tamaño += 1
            else:
                self._insertar_recursivo(nodo.derecha, dato, criterio)

    def buscar(self, criterio_buscar):
        """
        Busca un nodo en el árbol.

        Args:
            criterio_buscar: Función (dato) -> True/False

        Returns:
            El dato encontrado, o None

        Complejidad: O(n) en peor caso

        Ejemplo:
            >>> arbol = ArbolBinario()
            >>> arbol.insertar("Novela", comparar)
            >>> arbol.insertar("Romance", comparar)
            >>> encontrado = arbol.buscar(lambda x: x == "Novela")
        """
        return self._buscar_recursivo(self.raiz, criterio_buscar)

    def _buscar_recursivo(self, nodo, criterio):
        """Busca recursivamente."""
        if nodo is None:
            return None

        if criterio(nodo.dato):
            return nodo.dato

        resultado = self._buscar_recursivo(nodo.izquierda, criterio)
        if resultado is not None:
            return resultado

        return self._buscar_recursivo(nodo.derecha, criterio)

    def recorrido_inorden(self):
        """
        Recorrido inorden (izquierda-raíz-derecha).
        Produce lista ordenada.

        Returns:
            Lista de datos en orden

        Complejidad: O(n)

        Ejemplo:
            Árbol:      2
                       / \
                      1   3

            Inorden: [1, 2, 3]
        """
        resultado = []
        self._inorden_recursivo(self.raiz, resultado)
        return resultado

    def _inorden_recursivo(self, nodo, resultado):
        """Recorrido inorden recursivo."""
        if nodo is None:
            return
        self._inorden_recursivo(nodo.izquierda, resultado)
        resultado.append(nodo.dato)
        self._inorden_recursivo(nodo.derecha, resultado)

    def recorrido_preorden(self):
        """
        Recorrido preorden (raíz-izquierda-derecha).

        Returns:
            Lista en orden de visita

        Complejidad: O(n)
        """
        resultado = []
        self._preorden_recursivo(self.raiz, resultado)
        return resultado

    def _preorden_recursivo(self, nodo, resultado):
        """Recorrido preorden recursivo."""
        if nodo is None:
            return
        resultado.append(nodo.dato)
        self._preorden_recursivo(nodo.izquierda, resultado)
        self._preorden_recursivo(nodo.derecha, resultado)

    def recorrido_postorden(self):
        """
        Recorrido postorden (izquierda-derecha-raíz).

        Returns:
            Lista en orden de visita

        Complejidad: O(n)
        """
        resultado = []
        self._postorden_recursivo(self.raiz, resultado)
        return resultado

    def _postorden_recursivo(self, nodo, resultado):
        """Recorrido postorden recursivo."""
        if nodo is None:
            return
        self._postorden_recursivo(nodo.izquierda, resultado)
        self._postorden_recursivo(nodo.derecha, resultado)
        resultado.append(nodo.dato)

    def obtener_altura(self):
        """
        Obtiene altura del árbol.

        Returns:
            int: Altura (0 si vacío, 1 si solo raíz)

        Complejidad: O(n)
        """
        return self._altura_recursiva(self.raiz)

    def _altura_recursiva(self, nodo):
        """Calcula altura recursivamente."""
        if nodo is None:
            return 0
        return 1 + max(self._altura_recursiva(nodo.izquierda),
                       self._altura_recursiva(nodo.derecha))

    def obtener_cantidad(self):
        """Obtiene cantidad de nodos."""
        return self.tamaño

    def esta_vacio(self):
        """¿Está vacío?"""
        return self.raiz is None

    def limpiar(self):
        """Vacía el árbol."""
        self.raiz = None
        self.tamaño = 0
