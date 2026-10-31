"""
Clase Inventario — M02

Representa la disponibilidad de recursos en cada sede.
Es una matriz [sede][recurso] = cantidad disponible.

Estructura:
    inventario[i][j] = cantidad del recurso j en la sede i

    Ej:
              Libro1  Libro2  Equipo1  Sala1
    Sede1       2       1        1       1
    Sede2       1       3        0       1
    Sede3       0       2        2       0

Operaciones:
    - obtener_disponibilidad(recurso, sede): Cuántos hay
    - decrementar(recurso, sede): Alguien lo tomó (préstamo)
    - incrementar(recurso, sede): Se devolvió
    - mostrar_matriz(): Ver inventario completo
"""


class Inventario:
    """
    Matriz de disponibilidad de recursos por sede.

    Atributos:
        matriz (list[list[int]]): Matriz [sede][recurso] = cantidad
        num_sedes (int): Cantidad de sedes
        num_recursos (int): Cantidad de recursos únicos
        mapeo_recursos (dict): {código_recurso: índice_columna}
        mapeo_sedes (dict): {nombre_sede: índice_fila}

    Métodos:
        obtener_disponibilidad(codigo_recurso, sede): Cantidad disponible
        decrementar(codigo_recurso, sede): Restar 1 (préstamo)
        incrementar(codigo_recurso, sede): Sumar 1 (devolución)
        actualizar(codigo_recurso, sede, cantidad): Establecer cantidad
        mostrar_matriz(): Ver tabla completa
        obtener_fila(sede): Todos los recursos de una sede
        obtener_columna(codigo_recurso): Disponibilidad en todas las sedes

    Ejemplo de uso:
        >>> inventario = Inventario(num_sedes=3, num_recursos=10)
        >>> inventario.registrar_recurso("R001", "Libro Python")
        >>> inventario.registrar_sede(0, "Sede Centro")
        >>> inventario.actualizar("R001", "Sede Centro", 5)  # Hay 5 libros
        >>>
        >>> disponibles = inventario.obtener_disponibilidad("R001", "Sede Centro")
        >>> print(disponibles)
        5
        >>>
        >>> inventario.decrementar("R001", "Sede Centro")  # Alguien lo prestó
        >>> disponibles = inventario.obtener_disponibilidad("R001", "Sede Centro")
        >>> print(disponibles)
        4
    """

    def __init__(self, num_sedes=5, num_recursos=50):
        """
        Inicializa matriz de inventario.

        Args:
            num_sedes (int): Cantidad de sedes (filas)
            num_recursos (int): Cantidad de recursos (columnas)
        """
        self.num_sedes = num_sedes
        self.num_recursos = num_recursos

        # Matriz inicializada en 0 (sin recursos)
        self.matriz = [[0 for _ in range(num_recursos)] for _ in range(num_sedes)]

        # Mapeos para traducir códigos a índices
        self.mapeo_recursos = {}  # {código: índice_columna}
        self.mapeo_sedes = {}     # {nombre_sede: índice_fila}
        self.contador_recursos = 0
        self.contador_sedes = 0

    def registrar_recurso(self, codigo_recurso, nombre_recurso):
        """
        Registra un nuevo tipo de recurso.
        Le asigna una columna en la matriz.

        Args:
            codigo_recurso (str): Código único del recurso (ej: "R001")
            nombre_recurso (str): Nombre para referencia

        Returns:
            int: Índice de columna asignado

        Ejemplo:
            >>> inventario = Inventario(3, 10)
            >>> idx = inventario.registrar_recurso("R001", "Libro Python")
            >>> print(idx)
            0
        """
        if self.contador_recursos >= self.num_recursos:
            raise ValueError(f"No hay más espacio para recursos (máximo: {self.num_recursos})")

        if codigo_recurso not in self.mapeo_recursos:
            idx = self.contador_recursos
            self.mapeo_recursos[codigo_recurso] = idx
            self.contador_recursos += 1
            return idx

        return self.mapeo_recursos[codigo_recurso]

    def registrar_sede(self, indice_fila, nombre_sede):
        """
        Registra una sede.
        Le asigna una fila en la matriz.

        Args:
            indice_fila (int): Índice de fila (0 a num_sedes-1)
            nombre_sede (str): Nombre de la sede

        Ejemplo:
            >>> inventario = Inventario(3, 10)
            >>> inventario.registrar_sede(0, "Sede Centro")
            >>> inventario.registrar_sede(1, "Sede Norte")
        """
        if indice_fila >= self.num_sedes:
            raise ValueError(f"Índice de sede inválido (máximo: {self.num_sedes-1})")

        self.mapeo_sedes[nombre_sede] = indice_fila

    def obtener_disponibilidad(self, codigo_recurso, sede):
        """
        Obtiene la cantidad disponible de un recurso en una sede.

        Args:
            codigo_recurso (str): Código del recurso
            sede (str): Nombre de la sede

        Returns:
            int: Cantidad disponible (0 si no existe)

        Complejidad: O(1)

        Ejemplo:
            >>> inventario = Inventario(2, 5)
            >>> inventario.registrar_recurso("R001", "Libro")
            0
            >>> inventario.registrar_sede(0, "Centro")
            >>> inventario.actualizar("R001", "Centro", 5)
            >>> cantidad = inventario.obtener_disponibilidad("R001", "Centro")
            >>> print(cantidad)
            5
        """
        if codigo_recurso not in self.mapeo_recursos or sede not in self.mapeo_sedes:
            return 0

        i = self.mapeo_sedes[sede]
        j = self.mapeo_recursos[codigo_recurso]
        return self.matriz[i][j]

    def decrementar(self, codigo_recurso, sede):
        """
        Decrementa la cantidad (alguien prestó).

        Args:
            codigo_recurso (str): Código del recurso
            sede (str): Nombre de la sede

        Returns:
            bool: True si se decrementó, False si no hay disponible

        Complejidad: O(1)

        Ejemplo:
            >>> inventario = Inventario(2, 5)
            >>> inventario.registrar_recurso("R001", "Libro")
            0
            >>> inventario.registrar_sede(0, "Centro")
            >>> inventario.actualizar("R001", "Centro", 5)
            >>> inventario.decrementar("R001", "Centro")
            True
            >>> cantidad = inventario.obtener_disponibilidad("R001", "Centro")
            >>> print(cantidad)
            4
        """
        if codigo_recurso not in self.mapeo_recursos or sede not in self.mapeo_sedes:
            return False

        i = self.mapeo_sedes[sede]
        j = self.mapeo_recursos[codigo_recurso]

        if self.matriz[i][j] > 0:
            self.matriz[i][j] -= 1
            return True
        return False

    def incrementar(self, codigo_recurso, sede):
        """
        Incrementa la cantidad (alguien devolvió).

        Args:
            codigo_recurso (str): Código del recurso
            sede (str): Nombre de la sede

        Returns:
            bool: True si se incrementó, False si no existe

        Complejidad: O(1)
        """
        if codigo_recurso not in self.mapeo_recursos or sede not in self.mapeo_sedes:
            return False

        i = self.mapeo_sedes[sede]
        j = self.mapeo_recursos[codigo_recurso]
        self.matriz[i][j] += 1
        return True

    def actualizar(self, codigo_recurso, sede, cantidad):
        """
        Establece la cantidad a un valor específico.
        Usado para inicializar inventario.

        Args:
            codigo_recurso (str): Código del recurso
            sede (str): Nombre de la sede
            cantidad (int): Nueva cantidad

        Returns:
            bool: True si se actualizó

        Ejemplo:
            >>> inventario = Inventario(2, 5)
            >>> inventario.registrar_recurso("R001", "Libro")
            0
            >>> inventario.registrar_sede(0, "Centro")
            >>> inventario.actualizar("R001", "Centro", 10)
            True
        """
        if codigo_recurso not in self.mapeo_recursos or sede not in self.mapeo_sedes:
            return False

        i = self.mapeo_sedes[sede]
        j = self.mapeo_recursos[codigo_recurso]
        self.matriz[i][j] = max(0, cantidad)  # No negativos
        return True

    def obtener_fila(self, sede):
        """
        Obtiene disponibilidad de todos los recursos en una sede.

        Args:
            sede (str): Nombre de la sede

        Returns:
            list: Cantidades de cada recurso en esa sede

        Complejidad: O(num_recursos)
        """
        if sede not in self.mapeo_sedes:
            return []

        i = self.mapeo_sedes[sede]
        return self.matriz[i][:self.contador_recursos]

    def obtener_columna(self, codigo_recurso):
        """
        Obtiene disponibilidad de un recurso en todas las sedes.

        Args:
            codigo_recurso (str): Código del recurso

        Returns:
            list: Cantidades en cada sede

        Complejidad: O(num_sedes)
        """
        if codigo_recurso not in self.mapeo_recursos:
            return []

        j = self.mapeo_recursos[codigo_recurso]
        return [self.matriz[i][j] for i in range(self.num_sedes)]

    def mostrar_matriz(self):
        """
        Retorna la matriz en formato legible.

        Returns:
            str: Representación de la matriz
        """
        sedes_ordenadas = sorted(self.mapeo_sedes.items(), key=lambda x: x[1])
        recursos_ordenados = sorted(self.mapeo_recursos.items(), key=lambda x: x[1])

        # Encabezado
        linea = "Sede\\Recurso".ljust(15)
        for cod, idx in recursos_ordenados:
            linea += f" | {cod}".ljust(8)
        resultado = linea + "\n"
        resultado += "-" * len(linea) + "\n"

        # Filas
        for nombre_sede, idx_fila in sedes_ordenadas:
            linea = nombre_sede[:15].ljust(15)
            for cod, idx_col in recursos_ordenados:
                cantidad = self.matriz[idx_fila][idx_col]
                linea += f" | {cantidad}".ljust(8)
            resultado += linea + "\n"

        return resultado

    def __str__(self):
        """Representación en string."""
        return f"Inventario({self.num_sedes} sedes × {self.contador_recursos} recursos)"
