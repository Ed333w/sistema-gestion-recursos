"""
Clase GestorInventario — M07 (PRINCIPAL) [Carpeta: M08_inventario para compatibilidad]

Gestiona la disponibilidad de recursos por sede.
Matriz 2D: [sede][recurso] = cantidad disponible.

Estructura:
    matriz[i][j] = cantidad del recurso j en la sede i

    Ejemplo:
              Libro1  Libro2  Equipo1  Sala1
    Sede1       2       1        1       1
    Sede2       1       3        0       1
    Sede3       0       2        2       0

Operaciones:
    - obtener_disponibilidad(recurso, sede): Cuántos hay
    - decrementar(recurso, sede): Alguien lo tomó
    - incrementar(recurso, sede): Se devolvió
    - actualizar(recurso, sede, cantidad): Establecer cantidad
    - mostrar_matriz(): Ver inventario completo
"""


class GestorInventario:
    """
    Gestiona matriz de disponibilidad de recursos por sede.

    CLASE PRINCIPAL DE M07 (Sedes se integraron en M02_recursos).

    Atributos:
        matriz (list[list[int]]): Matriz [sede][recurso] = cantidad
        num_sedes (int): Cantidad de sedes
        num_recursos (int): Cantidad de recursos únicos
        mapeo_recursos (dict): {código_recurso: índice_columna}
        mapeo_sedes (dict): {nombre_sede: índice_fila}

    Métodos principales:
        obtener_disponibilidad: Cantidad disponible O(1)
        decrementar: Restar 1 (préstamo) O(1)
        incrementar: Sumar 1 (devolución) O(1)
        actualizar: Establecer cantidad O(1)
        mostrar_matriz: Ver tabla completa

    Ejemplo:
        >>> inventario = GestorInventario(num_sedes=3, num_recursos=10)
        >>> inventario.registrar_recurso("R001", "Libro Python")
        >>> inventario.registrar_sede(0, "Sede Centro")
        >>> inventario.actualizar("R001", "Sede Centro", 5)
        >>>
        >>> cantidad = inventario.obtener_disponibilidad("R001", "Sede Centro")
        >>> print(cantidad)
        5
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

    def _redimensionar_columnas(self):
        """
        Duplica el número de columnas de la matriz (misma estrategia que VectorDinamico).

        Se crea una matriz nueva con el doble de columnas y se copian las
        cantidades celda por celda; las columnas nuevas quedan en 0.

        Complejidad: O(sedes × recursos) cuando ocurre. Como la capacidad se
        duplica, ocurre pocas veces (log n) y el registro queda en O(1) amortizado.
        """
        nueva_capacidad = max(1, self.num_recursos * 2)
        # Arreglo de bajo nivel de tamaño fijo por fila, igual que el que usa
        # VectorDinamico._redimensionar; no es una colección que crece con append.
        nueva_matriz = [[0] * nueva_capacidad for _ in range(self.num_sedes)]
        for i in range(self.num_sedes):
            for j in range(self.contador_recursos):
                nueva_matriz[i][j] = self.matriz[i][j]
        self.matriz = nueva_matriz
        self.num_recursos = nueva_capacidad

    def registrar_recurso(self, codigo_recurso, nombre_recurso):
        """
        Registra un nuevo tipo de recurso (le asigna una columna).

        Ya no hay tope de 100: si las columnas se llenan, la matriz crece
        (RNF: operar con 500+ registros). Si el recurso ya estaba registrado,
        devuelve su columna sin crecer.

        Complejidad: O(1) amortizado; O(sedes × recursos) en el registro que crece.
        """
        if codigo_recurso not in self.mapeo_recursos:
            # Antes se lanzaba ValueError aquí y el recurso 101 quedaba sin columna.
            if self.contador_recursos >= self.num_recursos:
                self._redimensionar_columnas()
            idx = self.contador_recursos
            self.mapeo_recursos[codigo_recurso] = idx
            self.contador_recursos += 1
            return idx

        return self.mapeo_recursos[codigo_recurso]

    def registrar_sede(self, indice_fila, nombre_sede):
        """Registra una sede. O(1)"""
        if indice_fila >= self.num_sedes:
            raise ValueError(f"Índice de sede inválido (máximo: {self.num_sedes-1})")

        self.mapeo_sedes[nombre_sede] = indice_fila

    def obtener_disponibilidad(self, codigo_recurso, sede):
        """Obtiene cantidad disponible. O(1)"""
        if codigo_recurso not in self.mapeo_recursos or sede not in self.mapeo_sedes:
            return 0

        i = self.mapeo_sedes[sede]
        j = self.mapeo_recursos[codigo_recurso]
        return self.matriz[i][j]

    def decrementar(self, codigo_recurso, sede):
        """Decrementa (alguien prestó). O(1)"""
        if codigo_recurso not in self.mapeo_recursos or sede not in self.mapeo_sedes:
            return False

        i = self.mapeo_sedes[sede]
        j = self.mapeo_recursos[codigo_recurso]

        if self.matriz[i][j] > 0:
            self.matriz[i][j] -= 1
            return True
        return False

    def incrementar(self, codigo_recurso, sede):
        """Incrementa (se devolvió). O(1)"""
        if codigo_recurso not in self.mapeo_recursos or sede not in self.mapeo_sedes:
            return False

        i = self.mapeo_sedes[sede]
        j = self.mapeo_recursos[codigo_recurso]
        self.matriz[i][j] += 1
        return True

    def actualizar(self, codigo_recurso, sede, cantidad):
        """Establece cantidad a valor específico. O(1)"""
        if codigo_recurso not in self.mapeo_recursos or sede not in self.mapeo_sedes:
            return False

        i = self.mapeo_sedes[sede]
        j = self.mapeo_recursos[codigo_recurso]
        self.matriz[i][j] = max(0, cantidad)
        return True

    def obtener_fila(self, sede):
        """Obtiene disponibilidad de todos los recursos en una sede. O(num_recursos)"""
        if sede not in self.mapeo_sedes:
            return []

        i = self.mapeo_sedes[sede]
        return self.matriz[i][:self.contador_recursos]

    def obtener_columna(self, codigo_recurso):
        """Obtiene disponibilidad de un recurso en todas las sedes. O(num_sedes)"""
        if codigo_recurso not in self.mapeo_recursos:
            return []

        j = self.mapeo_recursos[codigo_recurso]
        return [self.matriz[i][j] for i in range(self.num_sedes)]

    def mostrar_matriz(self):
        """Retorna matriz en formato legible. O(sedes × recursos)"""
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
        return f"GestorInventario({self.num_sedes} sedes × {self.contador_recursos} recursos)"
