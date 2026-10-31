"""
M02 — RECURSOS Y SEDES (ENTREGA 1)

Descripción:
    Administra el catálogo de recursos (libros, equipos, salas).
    Gestiona sedes donde se ubican los recursos (sin conectividad de grafo).

Clases principales:
    - Recurso: Clase base abstracta (padre)
    - Libro: Hereda de Recurso (tipo de recurso)
    - Equipo: Hereda de Recurso (tipo de recurso)
    - Sala: Hereda de Recurso (tipo de recurso)
    - Sede: Ubicación de recursos (ENTREGA 1 - sin grafo)
    - Inventario: Matriz sede × tipo de recurso
    - GestorRecursos: Administra colección (PRINCIPAL)

Herencia:
    Recurso (base)
      ├── Libro (autor, ISBN, año_publicación)
      ├── Equipo (tipo, modelo, estado)
      └── Sala (capacidad, recursos_disponibles)

Estructuras usadas:
    - VectorDinamico: Almacenar recursos
    - Matriz: Disponibilidad [sede][tipo_recurso] = cantidad

Requerimientos que resuelve:
    - M02-R01: Registrar recurso (libro, equipo, sala)
    - M02-R02: Consultar disponibilidad por sede
    - M02-R03: Actualizar estado de recurso
    - M02-R04: Dar de baja recurso
    - M02-R05: Listar recursos por tipo
    - M02-R06: Ver inventario (matriz completa)

Ejemplo de uso:
    >>> gestor = GestorRecursos(num_sedes=3)
    >>>
    >>> # Registrar recursos
    >>> cod1 = gestor.registrar_libro("Python 101", "Guido", "978-123")
    >>> cod2 = gestor.registrar_equipo("Computador", "Dell XPS", "Sede 1")
    >>> cod3 = gestor.registrar_sala(30, "Sala de Estudio", "Sede 1")
    >>>
    >>> # Consultar disponibilidad
    >>> disponible = gestor.obtener_disponibilidad(cod1, "Sede 1")
    >>> print(disponible)
    1
    >>>
    >>> # Ver inventario
    >>> gestor.mostrar_inventario()
"""

from .recurso import Recurso
from .libro import Libro
from .equipo import Equipo
from .sala import Sala
from .sede import Sede
from .inventario import Inventario
from .gestor_recursos import GestorRecursos

__all__ = [
    'Recurso',
    'Libro',
    'Equipo',
    'Sala',
    'Sede',
    'Inventario',
    'GestorRecursos',
]
