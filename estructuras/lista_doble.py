"""
LISTA ENLAZADA DOBLE — Estructura de datos propia

Descripción:
    Estructura basada en nodos, donde cada nodo apunta al siguiente Y al anterior.
    Usado en M03 para historial de préstamos (navegación bidireccional).

Ventajas vs Lista Simple:
    - Navegación hacia adelante Y hacia atrás
    - Inserción más eficiente si tienes referencia al nodo

Desventajas:
    - Más memoria (dos apuntadores por nodo)
    - Más complejo de mantener

Funcionalidad:
    - Agregar al inicio: O(1)
    - Agregar al final: O(n) o O(1) si mantenemos cola
    - Buscar: O(n)
    - Recorrer hacia adelante: O(n)
    - Recorrer hacia atrás: O(n)

Requerimientos que resuelve:
    - M03: Historial de préstamos navegable en ambos sentidos
          "¿Cuál fue mi préstamo anterior?"
          "¿Cuál será el siguiente?"
"""


class NodoDoble:
    """
    Nodo para lista enlazada doble.

    Atributos:
        dato: El valor almacenado
        siguiente: Referencia al siguiente nodo
        anterior: Referencia al anterior nodo
    """

    def __init__(self, dato):
        """
        Crea un nodo con un dato.

        Args:
            dato: Valor a almacenar
        """
        self.dato = dato
        self.siguiente = None
        self.anterior = None

    def __str__(self):
        return f"NodoDoble({self.dato})"


class ListaDoble:
    """
    Lista enlazada doble.

    Atributos:
        cabeza (NodoDoble): Primer nodo
        cola (NodoDoble): Último nodo
        tamaño (int): Cantidad de nodos

    Métodos principales:
        agregar_al_inicio(dato): Insertar al principio
        agregar_al_final(dato): Insertar al final (O(1) con cola)
        eliminar_inicio(): Quitar el primer nodo
        eliminar_final(): Quitar el último nodo
        buscar(criterio_fn): Buscar nodo que cumpla criterio
        recorrer_adelante(): Lista de datos hacia adelante
        recorrer_atras(): Lista de datos hacia atrás

    Ejemplo de uso en M03 (Préstamos):
        >>> historial = ListaDoble()
        >>> historial.agregar_al_final(prestamo1)
        >>> historial.agregar_al_final(prestamo2)
        >>> historial.agregar_al_final(prestamo3)

        # Ver histórico hacia adelante
        >>> for p in historial.recorrer_adelante():
        ...     print(p.codigo)
        # Output: P001, P002, P003

        # Ver histórico hacia atrás (desde el más reciente)
        >>> for p in historial.recorrer_atras():
        ...     print(p.codigo)
        # Output: P003, P002, P001
    """

    def __init__(self):
        """Inicializa lista vacía."""
        self.cabeza = None
        self.cola = None
        self.tamaño = 0

    def agregar_al_inicio(self, dato):
        """
        Agrega elemento al inicio.

        Args:
            dato: Elemento a agregar

        Complejidad: O(1)
        """
        nuevo_nodo = NodoDoble(dato)

        if self.cabeza is None:
            self.cabeza = self.cola = nuevo_nodo
        else:
            nuevo_nodo.siguiente = self.cabeza
            self.cabeza.anterior = nuevo_nodo
            self.cabeza = nuevo_nodo

        self.tamaño += 1

    def agregar_al_final(self, dato):
        """
        Agrega elemento al final.

        Args:
            dato: Elemento a agregar

        Complejidad: O(1) porque mantenemos referencia a cola

        Nota: En M03, usamos esta operación para añadir cada préstamo
              al histórico en orden cronológico.
        """
        nuevo_nodo = NodoDoble(dato)

        if self.cola is None:
            self.cabeza = self.cola = nuevo_nodo
        else:
            nuevo_nodo.anterior = self.cola
            self.cola.siguiente = nuevo_nodo
            self.cola = nuevo_nodo

        self.tamaño += 1

    def eliminar_inicio(self):
        """
        Elimina el primer nodo.

        Returns:
            El dato del nodo eliminado, o None

        Complejidad: O(1)
        """
        if self.cabeza is None:
            return None

        dato = self.cabeza.dato

        if self.cabeza == self.cola:
            self.cabeza = self.cola = None
        else:
            self.cabeza = self.cabeza.siguiente
            self.cabeza.anterior = None

        self.tamaño -= 1
        return dato

    def eliminar_final(self):
        """
        Elimina el último nodo.

        Returns:
            El dato del nodo eliminado, o None

        Complejidad: O(1)
        """
        if self.cola is None:
            return None

        dato = self.cola.dato

        if self.cabeza == self.cola:
            self.cabeza = self.cola = None
        else:
            self.cola = self.cola.anterior
            self.cola.siguiente = None

        self.tamaño -= 1
        return dato

    def buscar(self, criterio_fn):
        """
        Busca el primer nodo (desde cabeza) que cumpla criterio.

        Args:
            criterio_fn: Función que toma un dato y retorna True/False

        Returns:
            El dato encontrado, o None

        Complejidad: O(n)

        Ejemplo:
            >>> lista = ListaDoble()
            >>> lista.agregar_al_final({'codigo': 'P001', 'usuario': 'Carlos'})
            >>> lista.agregar_al_final({'codigo': 'P002', 'usuario': 'Ana'})
            >>> prestamo = lista.buscar(lambda p: p['usuario'] == 'Carlos')
            >>> print(prestamo['codigo'])
            'P001'
        """
        actual = self.cabeza
        while actual is not None:
            if criterio_fn(actual.dato):
                return actual.dato
            actual = actual.siguiente
        return None

    def recorrer_adelante(self):
        """
        Obtiene lista de datos hacia adelante (cabeza → cola).

        Returns:
            Lista con los datos en orden

        Complejidad: O(n)

        Ejemplo en M03:
            >>> historial = ListaDoble()
            >>> for p in [1, 2, 3]:
            ...     historial.agregar_al_final(p)
            >>> historial.recorrer_adelante()
            [1, 2, 3]
        """
        resultado = []
        actual = self.cabeza
        while actual is not None:
            resultado.append(actual.dato)
            actual = actual.siguiente
        return resultado

    def recorrer_atras(self):
        """
        Obtiene lista de datos hacia atrás (cola → cabeza).

        Returns:
            Lista con los datos en orden inverso

        Complejidad: O(n)

        Ejemplo en M03:
            >>> historial = ListaDoble()
            >>> for p in [1, 2, 3]:
            ...     historial.agregar_al_final(p)
            >>> historial.recorrer_atras()
            [3, 2, 1]

        Uso real:
            "Mostrar mis últimos 3 préstamos" → recorrer_atras()[:3]
        """
        resultado = []
        actual = self.cola
        while actual is not None:
            resultado.append(actual.dato)
            actual = actual.anterior
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
        self.cola = None
        self.tamaño = 0

    def __str__(self):
        """Representación en string."""
        return f"ListaDoble({self.recorrer_adelante()})"

    def __repr__(self):
        """Representación para debug."""
        return self.__str__()
