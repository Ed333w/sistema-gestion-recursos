#!/usr/bin/env python3
"""
PRUEBAS BÁSICAS — Verificar funcionamiento de Entrega 1

Ejecutar:
    python pruebas/test_basico.py

Verifica:
    ✅ Estructuras de datos propias
    ✅ Modelo de clases con herencia
    ✅ Operaciones CRUD en M01 y M02
    ✅ Matriz de inventario
"""

import sys
import os

# Agregar la carpeta raíz al path para importaciones
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from estructuras import (VectorDinamico, ListaSimple, ListaDoble,
                         Pila, ColaFIFO)
from modulos import GestorUsuarios, GestorRecursos, Libro, Equipo, Sala


def test_vector_dinamico():
    """Prueba VectorDinamico."""
    print("\n🧪 TEST 1: Vector Dinámico")
    print("-" * 50)

    vector = VectorDinamico(capacidad_inicial=2)
    assert vector.obtener_tamaño() == 0, "Vector debe estar vacío"

    vector.agregar("A")
    vector.agregar("B")
    assert vector.obtener_tamaño() == 2, "Debe tener 2 elementos"
    assert vector.obtener_capacidad() == 2, "Capacidad inicial 2"

    vector.agregar("C")  # Se redimensiona
    assert vector.obtener_tamaño() == 3, "Debe tener 3 elementos"
    assert vector.obtener_capacidad() == 4, "Capacidad debe duplicarse a 4"

    assert vector.obtener(0) == "A", "Índice 0 debe ser A"
    assert vector.obtener(2) == "C", "Índice 2 debe ser C"

    assert vector.buscar("B") == 1, "B está en índice 1"
    assert vector.buscar("Z") == -1, "Z no existe"

    vector.eliminar_por_indice(1)
    assert vector.obtener_tamaño() == 2, "Debe tener 2 elementos después de eliminar"
    assert vector.obtener(1) == "C", "Índice 1 debe ser C (se movió)"

    print("✅ Vector Dinámico: CORRECTO")
    return True


def test_lista_simple():
    """Prueba ListaSimple."""
    print("\n🧪 TEST 2: Lista Simple")
    print("-" * 50)

    lista = ListaSimple()
    assert lista.esta_vacia(), "Lista debe estar vacía"

    lista.agregar_al_inicio("A")
    lista.agregar_al_final("B")
    lista.agregar_al_final("C")

    assert lista.obtener_tamaño() == 3, "Debe tener 3 elementos"
    assert lista.recorrer() == ["A", "B", "C"], "Orden correcto"

    primer = lista.eliminar_inicio()
    assert primer == "A", "Debe eliminar A"
    assert lista.obtener_tamaño() == 2, "Debe tener 2 elementos"

    encontrado = lista.buscar(lambda x: x == "B")
    assert encontrado == "B", "Debe encontrar B"

    print("✅ Lista Simple: CORRECTO")
    return True


def test_lista_doble():
    """Prueba ListaDoble."""
    print("\n🧪 TEST 3: Lista Doble")
    print("-" * 50)

    lista = ListaDoble()
    lista.agregar_al_final(1)
    lista.agregar_al_final(2)
    lista.agregar_al_final(3)

    assert lista.recorrer_adelante() == [1, 2, 3], "Adelante correcto"
    assert lista.recorrer_atras() == [3, 2, 1], "Atrás correcto"

    lista.eliminar_inicio()
    assert lista.recorrer_adelante() == [2, 3], "Después de eliminar inicio"

    lista.eliminar_final()
    assert lista.recorrer_adelante() == [2], "Después de eliminar final"

    print("✅ Lista Doble: CORRECTO")
    return True


def test_pila():
    """Prueba Pila."""
    print("\n🧪 TEST 4: Pila (LIFO)")
    print("-" * 50)

    pila = Pila()
    assert pila.esta_vacia(), "Pila debe estar vacía"

    pila.push("Op1")
    pila.push("Op2")
    pila.push("Op3")

    assert pila.obtener_tamaño() == 3, "Debe tener 3 elementos"
    assert pila.peek() == "Op3", "Tope debe ser Op3"

    sacado = pila.pop()
    assert sacado == "Op3", "Pop debe sacar Op3"
    assert pila.obtener_tamaño() == 2, "Debe tener 2 elementos"
    assert pila.peek() == "Op2", "Nuevo tope Op2"

    print("✅ Pila: CORRECTO")
    return True


def test_cola_fifo():
    """Prueba ColaFIFO."""
    print("\n🧪 TEST 5: Cola FIFO")
    print("-" * 50)

    cola = ColaFIFO()
    assert cola.esta_vacia(), "Cola debe estar vacía"

    cola.encolar("User1")
    cola.encolar("User2")
    cola.encolar("User3")

    assert cola.obtener_tamaño() == 3, "Debe tener 3 elementos"
    assert cola.frente() == "User1", "Frente debe ser User1"

    sacado = cola.desencolar()
    assert sacado == "User1", "Desencolar debe sacar User1"
    assert cola.obtener_tamaño() == 2, "Debe tener 2 elementos"
    assert cola.recorrer() == ["User2", "User3"], "Orden correcto"

    print("✅ Cola FIFO: CORRECTO")
    return True


def test_herencia():
    """Prueba herencia: Recurso → Libro, Equipo, Sala."""
    print("\n🧪 TEST 6: Herencia (Recurso → Libro, Equipo, Sala)")
    print("-" * 50)

    # Crear instancias de cada tipo
    libro = Libro("R001", "Python 101", "Guido", "978-123", 2020)
    equipo = Equipo("R002", "Proyector", "Proyector", "Epson", "Sala A")
    sala = Sala("R003", "Sala Est", 30, ["Mesas", "Sillas"])

    # Verificar que todos son Recurso (herencia funciona)
    assert libro.obtener_tipo() == "Libro", "Tipo debe ser Libro"
    assert equipo.obtener_tipo() == "Equipo", "Tipo debe ser Equipo"
    assert sala.obtener_tipo() == "Sala", "Tipo debe ser Sala"

    # Verificar atributos específicos
    assert libro.autor == "Guido", "Libro debe tener autor"
    assert equipo.modelo == "Epson", "Equipo debe tener modelo"
    assert sala.capacidad == 30, "Sala debe tener capacidad"

    # Verificar métodos heredados funcionan
    assert libro.es_disponible(), "Libro debe estar disponible"
    libro.marcar_no_disponible()
    assert not libro.es_disponible(), "Libro no disponible"

    libro.registrar_prestamo()
    assert libro.obtener_cantidad_prestamos() == 1, "Debe contar préstamo"

    print("✅ Herencia: CORRECTO")
    return True


def test_gestor_usuarios():
    """Prueba M01: Gestor de Usuarios."""
    print("\n🧪 TEST 7: M01 - Gestor de Usuarios")
    print("-" * 50)

    gestor = GestorUsuarios()
    assert gestor.obtener_cantidad() == 0, "Debe estar vacío"

    # Alta (Create)
    cod1 = gestor.registrar("Carlos", "carlos@uni.edu")
    cod2 = gestor.registrar("Ana", "ana@uni.edu")
    assert cod1 == "U001", "Primer código debe ser U001"
    assert cod2 == "U002", "Segundo código debe ser U002"
    assert gestor.obtener_cantidad() == 2, "Debe tener 2 usuarios"

    # Lectura (Read)
    usuario = gestor.buscar_por_codigo("U001")
    assert usuario is not None, "Debe encontrar U001"
    assert usuario.nombre == "Carlos", "Nombre debe ser Carlos"

    # Actualización (Update)
    gestor.actualizar("U001", "carlos.new@uni.edu")
    usuario = gestor.buscar_por_codigo("U001")
    assert usuario.email == "carlos.new@uni.edu", "Email debe actualizarse"

    # Baja (Delete lógica)
    gestor.dar_de_baja("U001")
    usuario = gestor.buscar_por_codigo("U001")
    assert usuario.estado == "Inactivo", "Debe estar inactivo"

    # Listado
    todos = gestor.listar_todos()
    assert len(todos) == 2, "Debe haber 2 usuarios (uno inactivo)"

    activos = gestor.listar_activos()
    assert len(activos) == 1, "Debe haber 1 activo"

    print("✅ Gestor de Usuarios: CORRECTO")
    return True


def test_gestor_recursos():
    """Prueba M02: Gestor de Recursos."""
    print("\n🧪 TEST 8: M02 - Gestor de Recursos")
    print("-" * 50)

    gestor = GestorRecursos(num_sedes=2)
    assert gestor.obtener_cantidad() == 0, "Debe estar vacío"

    # Registrar sedes
    gestor.registrar_sede(0, "Centro")
    gestor.registrar_sede(1, "Norte")

    # Alta de recursos (diferentes tipos)
    cod_libro = gestor.registrar_libro("Python", "Guido", "978-123", 2020)
    cod_equipo = gestor.registrar_equipo("Proyector", "Proyector", "Epson", "Sala")
    cod_sala = gestor.registrar_sala("Sala Est", 30)

    assert gestor.obtener_cantidad() == 3, "Debe tener 3 recursos"

    # Lectura
    recurso = gestor.buscar_por_codigo(cod_libro)
    assert recurso is not None, "Debe encontrar recurso"
    assert recurso.obtener_tipo() == "Libro", "Debe ser Libro"

    # Inventario
    gestor.actualizar_disponibilidad(cod_libro, "Centro", 5)
    disponible = gestor.obtener_disponibilidad(cod_libro, "Centro")
    assert disponible == 5, "Debe tener 5 libros en Centro"

    # Decrementar (préstamo)
    gestor.decrementar_disponibilidad(cod_libro, "Centro")
    disponible = gestor.obtener_disponibilidad(cod_libro, "Centro")
    assert disponible == 4, "Debe quedar 4 libros"

    # Incrementar (devolución)
    gestor.incrementar_disponibilidad(cod_libro, "Centro")
    disponible = gestor.obtener_disponibilidad(cod_libro, "Centro")
    assert disponible == 5, "Debe volver a 5 libros"

    # Listar por tipo
    libros = gestor.listar_por_tipo("Libro")
    assert len(libros) == 1, "Debe haber 1 libro"

    equipos = gestor.listar_por_tipo("Equipo")
    assert len(equipos) == 1, "Debe haber 1 equipo"

    print("✅ Gestor de Recursos: CORRECTO")
    return True


def main():
    """Ejecuta todas las pruebas."""
    print("\n" + "=" * 70)
    print("PRUEBAS BÁSICAS — ENTREGA 1")
    print("=" * 70)

    pruebas = [
        ("Vector Dinámico", test_vector_dinamico),
        ("Lista Simple", test_lista_simple),
        ("Lista Doble", test_lista_doble),
        ("Pila", test_pila),
        ("Cola FIFO", test_cola_fifo),
        ("Herencia", test_herencia),
        ("Gestor Usuarios (M01)", test_gestor_usuarios),
        ("Gestor Recursos (M02)", test_gestor_recursos),
    ]

    resultados = []
    for nombre, prueba in pruebas:
        try:
            resultado = prueba()
            resultados.append((nombre, resultado))
        except Exception as e:
            print(f"❌ {nombre}: ERROR")
            print(f"   {e}")
            resultados.append((nombre, False))

    # Resumen
    print("\n" + "=" * 70)
    print("RESUMEN")
    print("=" * 70)

    aprobadas = sum(1 for _, r in resultados if r)
    total = len(resultados)

    for nombre, resultado in resultados:
        estado = "✅ CORRECTO" if resultado else "❌ ERROR"
        print(f"{estado}: {nombre}")

    print(f"\nTotal: {aprobadas}/{total} pruebas aprobadas")

    if aprobadas == total:
        print("\n🎉 ¡TODAS LAS PRUEBAS PASARON!")
        return 0
    else:
        print(f"\n⚠️  {total - aprobadas} prueba(s) fallaron")
        return 1


if __name__ == "__main__":
    sys.exit(main())
