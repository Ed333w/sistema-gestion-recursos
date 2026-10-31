"""
MÓDULOS DEL SISTEMA — Paquete raíz

Sistema de Gestión de Recursos Comunitarios en Red de Bibliotecas — STARTUP EDITION

MÓDULOS (8 TOTAL - Cada uno es una CLASE PRINCIPAL):
    - M01_usuarios: Administración de usuarios (GestorUsuarios)
    - M02_recursos: Catálogo + herencia + búsqueda + sedes básicas (GestorRecursos con TablaHash)
    - M03_prestamos: Ciclo de préstamos (GestorPrestamos)
    - M04_turnos: Turnos justos (GestorTurnos)
    - M05_categorias: Jerarquía de categorías árbol (GestorCategorias)
    - M06_informes: Reportes + listados + ordenamientos (GeneradorInformes)
    - M07_inventario: Matriz de disponibilidad [sede][recurso] (GestorInventario)
    - M08_sistema_inteligente: Features startup (SistemaInteligente)
        ├─ Recomendaciones IA
        ├─ Calificaciones
        ├─ Predicciones
        └─ Gamificación

Cada módulo es un PAQUETE (carpeta) con:
    - __init__.py: Documentación y exports
    - Clase principal (ej: GestorUsuarios en M01)

Flujo típico de uso:
    >>> from modulos.M01_usuarios import GestorUsuarios
    >>> from modulos.M02_recursos import GestorRecursos
    >>> from modulos.M03_prestamos import GestorPrestamos
    >>>
    >>> usuarios = GestorUsuarios()
    >>> recursos = GestorRecursos()
    >>> prestamos = GestorPrestamos()
    >>>
    >>> # Registrar usuario
    >>> cod_usuario = usuarios.registrar("Carlos", "carlos@uni.edu")
    >>>
    >>> # Registrar recurso
    >>> cod_recurso = recursos.registrar_libro("Python 101", "Guido van Rossum", "978-123")
    >>>
    >>> # Hacer préstamo
    >>> prestamos.realizar_prestamo(cod_usuario, cod_recurso, "M01")  # Sede Main

NOTA SOBRE ENTREGAS:
    - ENTREGA 1 (E1): Estructuras lineales + CRUD + búsqueda O(1) + sedes básicas
    - ENTREGA 2/3 (E2/E3): Grafo, DFS/BFS para conectividad de sedes, árbol AVL, balanceo

    Funcionalidades E1:
        ✓ M01: CRUD usuarios
        ✓ M02: CRUD recursos + sedes (sin conectividad)
        ✓ M03: Préstamos + undo con Pila
        ✓ M04: Turnos con ColaFIFO
        ✓ M05: Categorías con ArbolBinario
        ✓ M06: Informes + ordenamiento
        ✓ M07: Matriz inventario
        ✓ M08: Sistema inteligente

    Funcionalidades E2/3 (no implementadas aún):
        ⚠️  Conectividad de sedes (Grafo, DFS, BFS)
        ⚠️  Árbol AVL balanceado
        ⚠️  Algoritmos avanzados de búsqueda
"""

# Importar módulos BASE (M01-M08)
from .M01_usuarios import GestorUsuarios, Usuario
from .M02_recursos import GestorRecursos, Recurso, Libro, Equipo, Sala, Sede
from .M03_prestamos import GestorPrestamos, Prestamo
from .M04_turnos import GestorTurnos, Solicitud
from .M05_categorias import GestorCategorias, Categoria
from .M06_informes import GeneradorInformes
from .M07_inventario import GestorInventario
from .M08_sistema_inteligente import SistemaInteligente

__all__ = [
    # M01
    'GestorUsuarios',
    'Usuario',
    # M02 (con Sedes integradas)
    'GestorRecursos',
    'Recurso',
    'Libro',
    'Equipo',
    'Sala',
    'Sede',
    # M03
    'GestorPrestamos',
    'Prestamo',
    # M04
    'GestorTurnos',
    'Solicitud',
    # M05
    'GestorCategorias',
    'Categoria',
    # M06 (Reportes + listados + ordenamientos)
    'GeneradorInformes',
    # M07 (Matriz de disponibilidad)
    'GestorInventario',
    # M08 (STARTUP - IA+Community+Analytics+Gamificación)
    'SistemaInteligente',
]
