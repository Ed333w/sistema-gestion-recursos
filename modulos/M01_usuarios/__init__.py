"""
M01 — GESTIÓN DE USUARIOS

Descripción:
    Administra el padrón de usuarios del sistema.
    Registra, consulta, actualiza y da de baja usuarios.
    Localiza usuarios por código en tiempo constante (con tabla hash en M05).

Clases principales:
    - Usuario: Representa un usuario del sistema
    - GestorUsuarios: Administra la colección de usuarios

Estructuras usadas:
    - VectorDinamico: Almacenar usuarios sin límite previo
    - TablaHash (M05): Índice rápido por código de usuario

Requerimientos que resuelve:
    - M01-R01: Registrar usuario (nombre, email, tipo)
    - M01-R02: Consultar usuario por código
    - M01-R03: Actualizar datos de usuario
    - M01-R04: Dar de baja usuario
    - M01-R05: Listar todos los usuarios
    - M01-R06: Verificar disponibilidad de código único

Ejemplo de uso:
    >>> gestor = GestorUsuarios()
    >>> gestor.registrar("Carlos López", "carlos@uni.edu")
    'U001'
    >>> usuario = gestor.buscar_por_codigo("U001")
    >>> print(usuario.nombre)
    'Carlos López'
    >>> gestor.actualizar("U001", "carlos.lopez@uni.edu")
    True
    >>> gestor.dar_de_baja("U001")
    True
"""

from .usuario import Usuario
from .gestor_usuarios import GestorUsuarios

__all__ = ['Usuario', 'GestorUsuarios']
