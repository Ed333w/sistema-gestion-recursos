"""
ESTRUCTURAS DE DATOS PROPIAS — Módulo de acceso

Implementaciones manuales de estructuras lineales, de acceso directo y complejas:

ENTREGA 1 (Estructuras lineales):
    - VectorDinamico: Arreglo que crece automáticamente (M01, M02)
    - ListaSimple: Nodos enlazados unidireccionales (M03)
    - ListaDoble: Nodos enlazados bidireccionales (M03)
    - Pila: Stack LIFO para deshacer (M03)
    - ColaFIFO: Queue para turnos justos (M04)

ENTREGA 2 (Acceso directo y búsqueda):
    - TablaHash: Búsqueda O(1) por código (M05)
    - ArbolBinario: Árbol binario básico (M07, sin balanceo AVL)

ENTREGA 2/3 (Grafos):
    - GrafoBasico: Grafo simple no dirigido (M08, conexión de sedes)

Cada estructura está completamente documentada con:
    - Descripción de funcionalidad
    - Complejidad de tiempo
    - Aplicaciones en los módulos
    - Ejemplos de uso
    - Casos de prueba
"""

# Estructuras de Entrega 1
from .vector_dinamico import VectorDinamico
from .lista_simple import ListaSimple, NodoSimple
from .lista_doble import ListaDoble, NodoDoble
from .pila import Pila
from .cola_fifo import ColaFIFO

# Estructuras de Entrega 2
from .tabla_hash import TablaHash
from .arbol_binario import ArbolBinario, NodoArbol
from .grafo import Grafo as GrafoBasico

__all__ = [
    # Entrega 1
    'VectorDinamico',
    'ListaSimple',
    'NodoSimple',
    'ListaDoble',
    'NodoDoble',
    'Pila',
    'ColaFIFO',
    # Entrega 2
    'TablaHash',
    'ArbolBinario',
    'NodoArbol',
    # Entrega 2/3
    'GrafoBasico',
]
