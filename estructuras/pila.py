"""
PILA (STACK) — Estructura de datos propia

Descripción:
    Estructura LIFO: Last In, First Out.
    El último elemento agregado es el primero en salir.
    Usado en M03 para deshacer última operación.

Implementación:
    Arreglo preallocado de tamaño dinámico (sin usar list nativa).
    Redimensionamiento automático cuando alcanza capacidad.

Complejidad:
    - push(elemento): O(1) amortizado
    - pop(): O(1)
    - peek(): O(1)
"""


class Pila:
    """
    Pila (estructura LIFO) implementada con arreglo dinámico.

    Atributos:
        datos (arreglo): Almacena los elementos
        tope (int): Posición del elemento en el tope
        capacidad (int): Capacidad actual del arreglo

    Métodos principales:
        push(dato): Agregar al tope
        pop(): Quitar del tope
        peek(): Ver tope sin quitar
        esta_vacia(): ¿Está vacía?
    """

    def __init__(self, capacidad_inicial=10):
        """Inicializa pila vacía con capacidad inicial."""
        self.capacidad = capacidad_inicial
        self.datos = [None] * capacidad_inicial  # Arreglo preallocado
        self.tope = 0  # Índice donde irá el próximo elemento

    def _redimensionar(self):
        """Duplica la capacidad cuando se llena."""
        nueva_capacidad = self.capacidad * 2
        nuevo_arreglo = [None] * nueva_capacidad

        # Copiar elementos existentes
        for i in range(self.tope):
            nuevo_arreglo[i] = self.datos[i]

        self.datos = nuevo_arreglo
        self.capacidad = nueva_capacidad

    def push(self, dato):
        """Agrega elemento al tope. O(1) amortizado."""
        if self.tope >= self.capacidad:
            self._redimensionar()

        self.datos[self.tope] = dato
        self.tope += 1

    def pop(self):
        """Quita y retorna elemento del tope. O(1)."""
        if self.tope == 0:
            return None

        self.tope -= 1
        resultado = self.datos[self.tope]
        self.datos[self.tope] = None  # Limpiar referencia
        return resultado

    def peek(self):
        """Retorna elemento del tope sin quitarlo. O(1)."""
        if self.tope == 0:
            return None
        return self.datos[self.tope - 1]

    def esta_vacia(self):
        """Verifica si pila está vacía. O(1)."""
        return self.tope == 0

    def obtener_tamaño(self):
        """Obtiene cantidad de elementos. O(1)."""
        return self.tope

    def limpiar(self):
        """Vacía la pila. O(1)."""
        self.tope = 0

    def recorrer(self):
        """Obtiene elementos de tope a base. O(n)."""
        resultado = []
        for i in range(self.tope - 1, -1, -1):
            resultado.append(self.datos[i])
        return resultado

    def __str__(self):
        """Representación en string."""
        return f"Pila(tamaño={self.tope}, capacidad={self.capacidad})"

    def __repr__(self):
        """Representación para debug."""
        return self.__str__()
