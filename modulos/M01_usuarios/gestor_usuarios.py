"""
Clase GestorUsuarios — M01 (PRINCIPAL)

Gestiona la colección de usuarios del sistema.

Estructura interna:
    - usuarios: VectorDinamico de objetos Usuario
    - contador_codigos: Genera códigos únicos (U001, U002, ...)

Operaciones:
    - registrar: Agregar nuevo usuario (Alta)
    - buscar_por_codigo: Encontrar por código (Consulta) - O(n) ahora, O(1) en M05
    - actualizar: Cambiar email (Actualización)
    - dar_de_baja: Marcar inactivo (Baja)
    - listar_todos: Ver todos los usuarios (Recorrido)
    - obtener_cantidad: Cuántos usuarios hay

Dependencias:
    - Usa: VectorDinamico, Usuario
    - Usado por: M03 (Préstamos), M04 (Turnos)
    - Sincroniza índice con: M05 (TablaHash para búsqueda rápida en Entrega 2)
"""

from estructuras import VectorDinamico
from .usuario import Usuario


class GestorUsuarios:
    """
    Administra todos los usuarios del sistema.

    Atributos:
        usuarios (VectorDinamico): Almacena objetos Usuario
        contador_codigos (int): Para generar códigos únicos
        codigos_usados (set): Códigos ya asignados (para validación rápida)

    Métodos principales (CRUD):
        registrar(nombre, email): Crear usuario (C - Create)
        buscar_por_codigo(codigo): Leer usuario (R - Read)
        actualizar(codigo, nuevo_email): Actualizar (U - Update)
        dar_de_baja(codigo): Eliminar lógicamente (D - Delete)
        listar_todos(): Leer todos (Read All)
        obtener_cantidad(): Estadística

    Ejemplo de uso completo:
        >>> gestor = GestorUsuarios()
        >>>
        >>> # Alta: Registrar usuarios
        >>> cod1 = gestor.registrar("Carlos López", "carlos@uni.edu")
        >>> cod2 = gestor.registrar("Ana García", "ana@uni.edu")
        >>> print(cod1, cod2)
        U001 U002
        >>>
        >>> # Lectura: Buscar usuario
        >>> usuario = gestor.buscar_por_codigo("U001")
        >>> print(usuario.nombre)
        Carlos López
        >>>
        >>> # Actualización
        >>> gestor.actualizar("U001", "carlos.lopez@uni.edu")
        >>>
        >>> # Listar todos
        >>> todos = gestor.listar_todos()
        >>> for u in todos:
        ...     print(f"{u.codigo}: {u.nombre} - {u.estado}")
        U001: Carlos López - Activo
        U002: Ana García - Activo
        >>>
        >>> # Baja lógica
        >>> gestor.dar_de_baja("U001")
        >>> usuario = gestor.buscar_por_codigo("U001")
        >>> print(usuario.estado)
        Inactivo
    """

    def __init__(self):
        """
        Inicializa el gestor de usuarios.

        Ejemplo:
            >>> gestor = GestorUsuarios()
            >>> print(gestor.obtener_cantidad())
            0
        """
        self.usuarios = VectorDinamico(capacidad_inicial=10)
        self.contador_codigos = 0
        self.codigos_usados = set()

    def registrar(self, nombre, email):
        """
        Registra un nuevo usuario.

        Args:
            nombre (str): Nombre completo del usuario
            email (str): Correo electrónico

        Returns:
            str: Código único asignado (ej: "U001")

        Raises:
            ValueError: Si nombre o email están vacíos

        Complejidad: O(1) amortizado (vector dinámico)

        Requerimiento: M01-R01 (Registrar usuario)

        Ejemplo:
            >>> gestor = GestorUsuarios()
            >>> codigo = gestor.registrar("Carlos López", "carlos@uni.edu")
            >>> print(codigo)
            'U001'
            >>> codigo2 = gestor.registrar("Ana García", "ana@uni.edu")
            >>> print(codigo2)
            'U002'
        """
        # Validar entrada
        if not nombre or (isinstance(nombre, str) and not nombre.strip()):
            raise ValueError("El nombre del usuario no puede estar vacío")
        if not email or (isinstance(email, str) and not email.strip()):
            raise ValueError("El email del usuario no puede estar vacío")

        # Generar código único
        self.contador_codigos += 1
        codigo = f"U{self.contador_codigos:03d}"  # U001, U002, ...

        # Crear usuario
        usuario = Usuario(codigo, nombre, email)

        # Almacenar en vector
        self.usuarios.agregar(usuario)
        self.codigos_usados.add(codigo)

        return codigo

    def buscar_por_codigo(self, codigo):
        """
        Busca un usuario por su código.

        Args:
            codigo (str): Código del usuario (ej: "U001")

        Returns:
            Usuario: El usuario encontrado, o None si no existe

        Complejidad: O(n) búsqueda lineal
        Nota: En Entrega 2, M05 proporciona O(1) con tabla hash

        Requerimiento: M01-R02 (Consultar usuario por código)

        Ejemplo:
            >>> gestor = GestorUsuarios()
            >>> codigo = gestor.registrar("Carlos", "carlos@uni.edu")
            >>> usuario = gestor.buscar_por_codigo(codigo)
            >>> print(usuario.nombre)
            'Carlos'
            >>> no_existe = gestor.buscar_por_codigo("U999")
            >>> print(no_existe)
            None
        """
        # Búsqueda lineal en vector
        usuarios_lista = self.usuarios.recorrer()
        for usuario in usuarios_lista:
            if usuario.codigo == codigo:
                return usuario
        return None

    def actualizar(self, codigo, nuevo_email):
        """
        Actualiza el email de un usuario.

        Args:
            codigo (str): Código del usuario
            nuevo_email (str): Nuevo email

        Returns:
            bool: True si se actualizó, False si usuario no existe

        Complejidad: O(n)

        Requerimiento: M01-R03 (Actualizar datos de usuario)

        Ejemplo:
            >>> gestor = GestorUsuarios()
            >>> cod = gestor.registrar("Carlos", "carlos@uni.edu")
            >>> gestor.actualizar(cod, "carlos.lopez@uni.edu")
            True
            >>> usuario = gestor.buscar_por_codigo(cod)
            >>> print(usuario.email)
            'carlos.lopez@uni.edu'
        """
        usuario = self.buscar_por_codigo(codigo)
        if usuario:
            usuario.actualizar_email(nuevo_email)
            return True
        return False

    def dar_de_baja(self, codigo):
        """
        Desactiva un usuario (baja lógica, no elimina).

        Args:
            codigo (str): Código del usuario

        Returns:
            bool: True si se deactivó, False si usuario no existe o tiene préstamos activos

        Raises:
            ValueError: Si el usuario tiene préstamos activos

        Complejidad: O(n)

        Requerimiento: M01-R04 (Dar de baja usuario)

        Nota: No eliminamos de la lista, solo marcamos como "Inactivo"
              para mantener historial y consistencia de códigos.
              No se puede dar de baja si tiene préstamos activos.

        Ejemplo:
            >>> gestor = GestorUsuarios()
            >>> cod = gestor.registrar("Carlos", "carlos@uni.edu")
            >>> gestor.dar_de_baja(cod)
            True
            >>> usuario = gestor.buscar_por_codigo(cod)
            >>> print(usuario.estado)
            'Inactivo'
        """
        usuario = self.buscar_por_codigo(codigo)
        if usuario:
            if usuario.cantidad_prestamos > 0:
                raise ValueError(f"No se puede dar de baja al usuario {codigo}: tiene {usuario.cantidad_prestamos} préstamo(s) activo(s)")
            usuario.dar_de_baja()
            return True
        return False

    def reactivar(self, codigo):
        """
        Reactiva un usuario inactivo.

        Args:
            codigo (str): Código del usuario

        Returns:
            bool: True si se reactivó, False si usuario no existe o ya es activo

        Complejidad: O(n)
        """
        usuario = self.buscar_por_codigo(codigo)
        if usuario and not usuario.es_activo():
            usuario.reactivar()
            return True
        return False

    def listar_todos(self):
        """
        Obtiene lista de todos los usuarios.

        Returns:
            list: Objetos Usuario en la colección

        Complejidad: O(n)

        Requerimiento: M01-R05 (Listar todos los usuarios)

        Ejemplo:
            >>> gestor = GestorUsuarios()
            >>> gestor.registrar("Carlos", "carlos@uni.edu")
            'U001'
            >>> gestor.registrar("Ana", "ana@uni.edu")
            'U002'
            >>> todos = gestor.listar_todos()
            >>> len(todos)
            2
            >>> for u in todos:
            ...     print(u)
            Usuario(U001: Carlos, carlos@uni.edu, Activo)
            Usuario(U002: Ana, ana@uni.edu, Activo)
        """
        return self.usuarios.recorrer()

    def listar_activos(self):
        """
        Obtiene lista de usuarios activos.

        Returns:
            list: Usuarios con estado "Activo"

        Complejidad: O(n)
        """
        todos = self.usuarios.recorrer()
        return [u for u in todos if u.es_activo()]

    def listar_inactivos(self):
        """
        Obtiene lista de usuarios inactivos.

        Returns:
            list: Usuarios con estado "Inactivo"

        Complejidad: O(n)
        """
        todos = self.usuarios.recorrer()
        return [u for u in todos if not u.es_activo()]

    def codigo_existe(self, codigo):
        """
        Verifica rápidamente si un código ya está usado.

        Args:
            codigo (str): Código a verificar

        Returns:
            bool: True si ya existe

        Complejidad: O(1)

        Requerimiento: M01-R06 (Verificar disponibilidad de código)
        """
        return codigo in self.codigos_usados

    def obtener_cantidad(self):
        """
        Obtiene la cantidad total de usuarios.

        Returns:
            int: Cantidad de usuarios registrados

        Complejidad: O(1)

        Ejemplo:
            >>> gestor = GestorUsuarios()
            >>> gestor.registrar("Carlos", "carlos@uni.edu")
            'U001'
            >>> gestor.registrar("Ana", "ana@uni.edu")
            'U002'
            >>> gestor.obtener_cantidad()
            2
        """
        return self.usuarios.obtener_tamaño()

    def obtener_cantidad_activos(self):
        """Obtiene cantidad de usuarios activos."""
        return len(self.listar_activos())

    def limpiar(self):
        """
        Elimina todos los usuarios (PELIGROSO, solo para testing).

        Complejidad: O(1)
        """
        self.usuarios.limpiar()
        self.contador_codigos = 0
        self.codigos_usados.clear()

    def __str__(self):
        """Representación en string."""
        activos = self.obtener_cantidad_activos()
        total = self.obtener_cantidad()
        return f"GestorUsuarios(total={total}, activos={activos})"
