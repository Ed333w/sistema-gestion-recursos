"""
COLA FIFO (QUEUE) — Estructura de datos propia

Descripción:
    Estructura FIFO: First In, First Out.
    El primer elemento agregado es el primero en salir.
    Usado en M04 para turnos justos.

Implementación:
    Arreglo circular para encolar y desencolar O(1) ambos.
    Redimensionamiento automático cuando llena.

Complejidad:
    - encolar(elemento): O(1) amortizado
    - desencolar(): O(1)
    - frente(): O(1)
"""


class ColaFIFO:
    """
    Cola FIFO (First In, First Out) con arreglo circular.

    Atributos:
        datos (arreglo): Almacena los elementos
        inicio (int): Índice del primer elemento
        fin (int): Índice donde irá el próximo elemento
        tamaño (int): Cantidad de elementos
        capacidad (int): Capacidad del arreglo

    Métodos principales:
        encolar(dato): Agregar al final
        desencolar(): Quitar del inicio
        frente(): Ver primero sin quitar
        esta_vacia(): ¿Está vacía?
    """

    def __init__(self, capacidad_inicial=10):
        """Inicializa cola vacía."""
        self.capacidad = capacidad_inicial
        self.datos = [None] * capacidad_inicial  # Arreglo preallocado
        self.inicio = 0
        self.fin = 0
        self.tamaño = 0

    def _redimensionar(self):
        """Duplica capacidad cuando se llena."""
        nueva_capacidad = self.capacidad * 2
        nuevo_arreglo = [None] * nueva_capacidad

        # Copiar elementos en orden
        for i in range(self.tamaño):
            idx_original = (self.inicio + i) % self.capacidad
            nuevo_arreglo[i] = self.datos[idx_original]

        self.datos = nuevo_arreglo
        self.inicio = 0
        self.fin = self.tamaño
        self.capacidad = nueva_capacidad

    def encolar(self, dato):
        """Agrega elemento al final. O(1) amortizado."""
        if self.tamaño >= self.capacidad:
            self._redimensionar()

        self.datos[self.fin] = dato
        self.fin = (self.fin + 1) % self.capacidad
        self.tamaño += 1

    def desencolar(self):
        """Quita y retorna primer elemento. O(1)."""
        if self.tamaño == 0:
            return None

        resultado = self.datos[self.inicio]
        self.datos[self.inicio] = None  # Limpiar referencia
        self.inicio = (self.inicio + 1) % self.capacidad
        self.tamaño -= 1
        return resultado

    def frente(self):
        """Retorna primer elemento sin quitarlo. O(1)."""
        if self.tamaño == 0:
            return None
        return self.datos[self.inicio]

    def esta_vacia(self):
        """Verifica si cola está vacía. O(1)."""
        return self.tamaño == 0

    def obtener_tamaño(self):
        """Obtiene cantidad de elementos. O(1)."""
        return self.tamaño

    def limpiar(self):
        """Vacía la cola. O(1)."""
        self.inicio = 0
        self.fin = 0
        self.tamaño = 0

    def recorrer(self):
        """Obtiene elementos en orden FIFO. O(n)."""
        resultado = []
        for i in range(self.tamaño):
            idx = (self.inicio + i) % self.capacidad
            resultado.append(self.datos[idx])
        return resultado

    def __str__(self):
        """Representación en string."""
        return f"ColaFIFO(tamaño={self.tamaño}, capacidad={self.capacidad})"

    def __repr__(self):
        """Representación para debug."""
        return self.__str__()
