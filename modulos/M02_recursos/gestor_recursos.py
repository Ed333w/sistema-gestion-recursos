"""
Clase GestorRecursos — M02 (PRINCIPAL)

Gestiona la colección de recursos (libros, equipos, salas).
Búsqueda rápida con TablaHash (anteriormente M05_indices).
Inventario delegado a M08 (GestorInventario).

Estructura:
    - recursos: VectorDinamico de objetos Recurso (Libro, Equipo, Sala)
    - indice: TablaHash para búsqueda O(1) por código
    - contador_codigos: Genera códigos únicos

Operaciones CRUD:
    - registrar_libro/registrar_equipo/registrar_sala: Crear (C)
    - buscar_por_codigo: Leer (R) - O(1) con TablaHash
    - dar_de_baja: Eliminar lógicamente (D)
    - listar_todos: Leer todos (R)

Nota: La gestión de inventario está en M08 (GestorInventario)
"""

from estructuras import VectorDinamico, TablaHash
from .recurso import Recurso
from .libro import Libro
from .equipo import Equipo
from .sala import Sala
from .sede import Sede
from modulos.M07_inventario import GestorInventario


class GestorRecursos:
    """
    Administra todos los recursos del sistema.

    Atributos:
        recursos (VectorDinamico): Almacena objetos Recurso
        indice (TablaHash): Índice rápido para búsqueda O(1)
        contador_codigos (int): Para generar códigos únicos
        codigos_usados (set): Códigos ya asignados
        sedes (TablaHash): Almacena sedes por código

    Métodos principales:
        registrar_libro: Crear un libro
        registrar_equipo: Crear un equipo
        registrar_sala: Crear una sala
        buscar_por_codigo: Encontrar recurso O(1) con TablaHash
        listar_todos: Ver todos los recursos
        listar_por_tipo: Ver solo libros, equipos, o salas
        registrar_sede: Registrar sede (sin grafo - ENTREGA 1)

    Nota: Conectividad de sedes (Grafo, DFS, BFS) se implementará en ENTREGA 2/3.

    Ejemplo:
        >>> gestor = GestorRecursos()
        >>> gestor.registrar_sede("S001", "Sede Centro")
        >>>
        >>> # Registrar recursos
        >>> cod_libro = gestor.registrar_libro("Python 101", "Guido", "978-123", 2020)
        >>> cod_equipo = gestor.registrar_equipo("Proyector 1", "Proyector", "Epson", "Sala A")
        >>> cod_sala = gestor.registrar_sala("Sala de Estudio", 30, ["Mesas", "Sillas"])
    """

    def __init__(self, num_sedes=10):
        """Inicializa gestor de recursos.

        Args:
            num_sedes: Número de sedes para el inventario
        """
        self.recursos = VectorDinamico(capacidad_inicial=20)
        self.indice = TablaHash(tamaño=100)  # Búsqueda O(1) por código
        self.contador_codigos = 0
        self.codigos_usados = set()
        # Gestión de sedes (ENTREGA 1 - sin conectividad de grafo)
        self.sedes = TablaHash(tamaño=50)
        self.contador_sedes = 0
        # Gestión de inventario (M07) - matriz de disponibilidad
        self.inventario = GestorInventario(num_sedes=num_sedes, num_recursos=100)

    def _generar_codigo(self):
        """Genera código único para recurso."""
        self.contador_codigos += 1
        codigo = f"R{self.contador_codigos:04d}"
        self.codigos_usados.add(codigo)
        return codigo

    def registrar_libro(self, nombre, autor, isbn, año_publicacion):
        """Registra un nuevo libro."""
        codigo = self._generar_codigo()
        libro = Libro(codigo, nombre, autor, isbn, año_publicacion)
        self.recursos.agregar(libro)
        self.indice.insertar(codigo, libro)  # Indexar para búsqueda O(1)
        return codigo

    def registrar_equipo(self, nombre, tipo_equipo, modelo, ubicacion):
        """Registra un nuevo equipo."""
        codigo = self._generar_codigo()
        equipo = Equipo(codigo, nombre, tipo_equipo, modelo, ubicacion)
        self.recursos.agregar(equipo)
        self.indice.insertar(codigo, equipo)  # Indexar para búsqueda O(1)
        return codigo

    def registrar_sala(self, nombre, capacidad, recursos_disponibles=None):
        """Registra una nueva sala."""
        codigo = self._generar_codigo()
        sala = Sala(codigo, nombre, capacidad, recursos_disponibles)
        self.recursos.agregar(sala)
        self.indice.insertar(codigo, sala)  # Indexar para búsqueda O(1)
        return codigo

    def buscar_por_codigo(self, codigo):
        """Busca un recurso por código. O(1) con TablaHash."""
        return self.indice.buscar(codigo)

    def dar_de_baja(self, codigo):
        """Desactiva un recurso."""
        recurso = self.buscar_por_codigo(codigo)
        if recurso:
            recurso.dar_de_baja()
            return True
        return False

    def listar_todos(self):
        """Obtiene todos los recursos."""
        return self.recursos.recorrer()

    def listar_por_tipo(self, tipo):
        """Obtiene recursos de un tipo específico."""
        todos = self.recursos.recorrer()
        return [r for r in todos if r.obtener_tipo() == tipo]

    def obtener_cantidad(self):
        """Total de recursos."""
        return self.recursos.obtener_tamaño()

    # ─── GESTIÓN DE SEDES (ENTREGA 1) ───

    def registrar_sede(self, indice_fila, nombre):
        """
        Registra una nueva sede.

        Args:
            indice_fila: int (índice en la matriz de inventario)
            nombre: str (Sede Centro, Sede Norte, etc.)

        Returns:
            str: nombre de la sede

        Complejidad: O(1) con TablaHash
        """
        codigo = f"S{indice_fila:03d}"
        sede = Sede(codigo, nombre)
        self.sedes.insertar(codigo, sede)
        self.contador_sedes += 1
        # Registrar sede en inventario
        self.inventario.registrar_sede(indice_fila, nombre)
        return nombre

    def obtener_sede(self, codigo):
        """
        Obtiene sede por código.

        Args:
            codigo: str

        Returns:
            Sede o None

        Complejidad: O(1) promedio
        """
        return self.sedes.buscar(codigo)

    def obtener_cantidad_sedes(self):
        """
        Obtiene cantidad de sedes registradas.

        Complejidad: O(1)
        """
        return self.contador_sedes

    def listar_sedes(self):
        """
        Lista todas las sedes registradas.

        Returns:
            list: Lista de objetos Sede

        Complejidad: O(n) donde n = cantidad de sedes
        """
        sedes = []
        for codigo in self.sedes.obtener_todas_las_claves():
            sede = self.sedes.buscar(codigo)
            if sede is not None:
                sedes.append(sede)
        return sedes

    # ─── GESTIÓN DE DISPONIBILIDAD (Delegada a GestorInventario) ───

    def registrar_recurso_en_inventario(self, codigo_recurso):
        """Registra un recurso en el inventario. O(1)"""
        recurso = self.buscar_por_codigo(codigo_recurso)
        if recurso:
            self.inventario.registrar_recurso(codigo_recurso, recurso.nombre)
            return True
        return False

    def actualizar_disponibilidad(self, codigo_recurso, sede, cantidad):
        """Actualiza disponibilidad de un recurso en una sede. O(1)"""
        self.registrar_recurso_en_inventario(codigo_recurso)
        return self.inventario.actualizar(codigo_recurso, sede, cantidad)

    def obtener_disponibilidad(self, codigo_recurso, sede):
        """Obtiene disponibilidad de un recurso en una sede. O(1)"""
        return self.inventario.obtener_disponibilidad(codigo_recurso, sede)

    def decrementar_disponibilidad(self, codigo_recurso, sede):
        """Decrementa disponibilidad (préstamo). O(1)"""
        return self.inventario.decrementar(codigo_recurso, sede)

    def incrementar_disponibilidad(self, codigo_recurso, sede):
        """Incrementa disponibilidad (devolución). O(1)"""
        return self.inventario.incrementar(codigo_recurso, sede)

    def __str__(self):
        """Representación."""
        libros = len(self.listar_por_tipo("Libro"))
        equipos = len(self.listar_por_tipo("Equipo"))
        salas = len(self.listar_por_tipo("Sala"))
        return f"GestorRecursos(libros={libros}, equipos={equipos}, salas={salas})"
