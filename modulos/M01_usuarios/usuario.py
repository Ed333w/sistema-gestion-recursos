"""
Clase Usuario — M01

Representa un usuario del sistema de bibliotecas.
Atributos:
    - código: Identificador único (ej: "U001", "U002")
    - nombre: Nombre completo
    - email: Correo electrónico
    - fecha_registro: Cuándo se registró
    - estado: Activo/Inactivo
    - cantidad_prestamos: Cuántos préstamos tiene activos
"""

from datetime import datetime


class Usuario:
    """
    Representa un usuario del sistema.

    Atributos:
        codigo (str): Identificador único (ej: "U001")
        nombre (str): Nombre completo (ej: "Carlos López")
        email (str): Email (ej: "carlos@uni.edu")
        fecha_registro (datetime): Fecha/hora de registro
        estado (str): "Activo" o "Inactivo"
        cantidad_prestamos (int): Cuántos préstamos tiene activos
        historial_prestamos (list): Códigos de préstamos realizados

    Métodos:
        __init__: Constructor
        registrar_prestamo: Agregar un préstamo
        devolver_prestamo: Quitar un préstamo
        obtener_info: Información del usuario
        es_activo: ¿Está activo?
        __str__: Representación en string
        __repr__: Para debug
    """

    def __init__(self, codigo, nombre, email):
        """
        Crea un usuario.

        Args:
            codigo (str): Identificador único (ej: "U001")
            nombre (str): Nombre completo
            email (str): Correo electrónico

        Ejemplo:
            >>> usuario = Usuario("U001", "Carlos López", "carlos@uni.edu")
            >>> print(usuario.codigo)
            'U001'
            >>> print(usuario.estado)
            'Activo'
        """
        self.codigo = codigo
        self.nombre = nombre
        self.email = email
        self.fecha_registro = datetime.now()
        self.estado = "Activo"
        self.cantidad_prestamos = 0
        self.historial_prestamos = []

    def registrar_prestamo(self, codigo_prestamo):
        """
        Registra un nuevo préstamo para este usuario.

        Args:
            codigo_prestamo (str): Código del préstamo (ej: "P001")

        Ejemplo:
            >>> usuario = Usuario("U001", "Carlos", "carlos@uni.edu")
            >>> usuario.registrar_prestamo("P001")
            >>> usuario.cantidad_prestamos
            1
            >>> "P001" in usuario.historial_prestamos
            True
        """
        if codigo_prestamo not in self.historial_prestamos:
            self.historial_prestamos.append(codigo_prestamo)
            self.cantidad_prestamos += 1

    def devolver_prestamo(self, codigo_prestamo):
        """
        Marca un préstamo como devuelto.

        Args:
            codigo_prestamo (str): Código del préstamo

        Returns:
            True si se encontró y se devolvió, False si no existe

        Ejemplo:
            >>> usuario = Usuario("U001", "Carlos", "carlos@uni.edu")
            >>> usuario.registrar_prestamo("P001")
            >>> usuario.devolver_prestamo("P001")
            True
            >>> usuario.cantidad_prestamos
            0
        """
        if codigo_prestamo in self.historial_prestamos:
            self.historial_prestamos.remove(codigo_prestamo)
            self.cantidad_prestamos = max(0, self.cantidad_prestamos - 1)
            return True
        return False

    def actualizar_email(self, nuevo_email):
        """
        Actualiza el correo del usuario.

        Args:
            nuevo_email (str): Nuevo correo electrónico

        Ejemplo:
            >>> usuario = Usuario("U001", "Carlos", "carlos@uni.edu")
            >>> usuario.actualizar_email("carlos.lopez@uni.edu")
            >>> usuario.email
            'carlos.lopez@uni.edu'
        """
        self.email = nuevo_email

    def dar_de_baja(self):
        """
        Marca usuario como inactivo.
        No lo elimina, solo lo desactiva.

        Ejemplo:
            >>> usuario = Usuario("U001", "Carlos", "carlos@uni.edu")
            >>> usuario.dar_de_baja()
            >>> usuario.estado
            'Inactivo'
            >>> usuario.es_activo()
            False
        """
        self.estado = "Inactivo"

    def reactivar(self):
        """
        Reactiva un usuario inactivo.

        Ejemplo:
            >>> usuario = Usuario("U001", "Carlos", "carlos@uni.edu")
            >>> usuario.dar_de_baja()
            >>> usuario.reactivar()
            >>> usuario.es_activo()
            True
        """
        self.estado = "Activo"

    def es_activo(self):
        """
        Verifica si el usuario está activo.

        Returns:
            bool: True si estado == "Activo"

        Ejemplo:
            >>> usuario = Usuario("U001", "Carlos", "carlos@uni.edu")
            >>> usuario.es_activo()
            True
            >>> usuario.dar_de_baja()
            >>> usuario.es_activo()
            False
        """
        return self.estado == "Activo"

    def obtener_info(self):
        """
        Obtiene información del usuario como diccionario.

        Returns:
            dict: Información del usuario

        Ejemplo:
            >>> usuario = Usuario("U001", "Carlos", "carlos@uni.edu")
            >>> info = usuario.obtener_info()
            >>> print(info['nombre'])
            'Carlos'
            >>> print(info['cantidad_prestamos'])
            0
        """
        return {
            'codigo': self.codigo,
            'nombre': self.nombre,
            'email': self.email,
            'estado': self.estado,
            'cantidad_prestamos': self.cantidad_prestamos,
            'fecha_registro': self.fecha_registro.strftime("%Y-%m-%d %H:%M:%S"),
            'prestamos_activos': self.historial_prestamos.copy()
        }

    def __str__(self):
        """Representación legible."""
        return f"Usuario({self.codigo}: {self.nombre}, {self.email}, {self.estado})"

    def __repr__(self):
        """Para debug."""
        return f"Usuario(codigo='{self.codigo}', nombre='{self.nombre}', email='{self.email}', estado='{self.estado}', prestamos={self.cantidad_prestamos})"

    def __eq__(self, otro):
        """Comparación por código."""
        if isinstance(otro, Usuario):
            return self.codigo == otro.codigo
        return False
