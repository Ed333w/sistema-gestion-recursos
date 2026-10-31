#!/usr/bin/env python3
"""
MAIN - Sistema de Gestion de Recursos Comunitarios

Menu interactivo con opciones de Entrega 1 + Funciones Inteligentes (Startup).

COMO EJECUTAR:
    python main.py
"""

import sys
from modulos import (GestorUsuarios, GestorRecursos, GestorPrestamos, GestorTurnos,
                     GestorCategorias, GeneradorInformes, GestorInventario, SistemaInteligente)
from modulos.M03_prestamos import SinUnidadesError
from estructuras import VectorDinamico, ListaSimple, ListaDoble, Pila, ColaFIFO


def limpiar_pantalla():
    """Limpia la pantalla de consola."""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def pausa():
    """Pausa y espera que el usuario presione Enter."""
    try:
        input("\nPresione Enter para continuar...")
    except EOFError:
        pass


def menu_principal():
    """Muestra el menu principal."""
    limpiar_pantalla()
    print("=" * 70)
    print("  SISTEMA DE GESTION DE RECURSOS COMUNITARIOS")
    print("  Red de Bibliotecas Universitarias - Startup Edition")
    print("=" * 70)
    print()
    print("═ MODULOS PRINCIPALES ═")
    print()
    print("  1. Gestion de Usuarios (M01)")
    print("     Registrar, listar, consultar usuarios")
    print()
    print("  2. Gestion de Recursos (M02)")
    print("     Registrar libros, equipos, salas con herencia")
    print()
    print("  3. Gestion de Inventario (M07)")
    print("     Ver matriz de disponibilidad por sede y recurso")
    print()
    print("  4. Gestion de Prestamos (M03)")
    print("     Registrar, devolver, deshacer, historial")
    print()
    print("  5. Gestion de Turnos (M04)")
    print("     Solicitar turno, ver turnos y fila de espera")
    print()
    print("  6. Gestion de Categorias (M05)")
    print("     Registrar y buscar categorías")
    print()
    print("  7. Informes y Reportes (M06)")
    print("     Reportes de uso e inventario")
    print()
    print("  8. Pruebas de Estructuras")
    print("     VectorDinamico, ListaSimple, ListaDoble, Pila, Cola")
    print()
    print("  9. Funciones Inteligentes (M08)")
    print()
    print("  0. Salir")
    print()


def menu_funciones_inteligentes(sistema_inteligente):
    """Submenu para funciones inteligentes del startup."""
    while True:
        limpiar_pantalla()
        print("  FUNCIONES INTELIGENTES ")
        print()
        print("  1. Recomendaciones Inteligentes")
        print("     (IA: Collaborative Filtering - Como Netflix)")
        print()
        print("  2. Calificaciones y Reviews")
        print("     (Community: Reviews 1-5 estrellas - Como Airbnb)")
        print()
        print("  3. Prediccion de Disponibilidad")
        print("     (Analytics: Forecast de cuando esta disponible)")
        print()
        print("  4. Gamificacion")
        print("     (Engagement: Puntos, Badges, Niveles, Leaderboards)")
        print()
        print("  0. Volver al menu principal")
        print()

        try:
            opcion = input("Selecciona opcion: ").strip()
        except EOFError:
            break

        if opcion == "0":
            break

        elif opcion == "1":
            demo_recomendaciones(sistema_inteligente)

        elif opcion == "2":
            demo_calificaciones(sistema_inteligente)

        elif opcion == "3":
            demo_prediccion(sistema_inteligente)

        elif opcion == "4":
            demo_gamificacion(sistema_inteligente)

        else:
            print("\nOpcion invalida")
            pausa()


def demo_recomendaciones(sistema):
    """Demostracion de recomendaciones inteligentes."""
    limpiar_pantalla()
    print("  RECOMENDACIONES INTELIGENTES (IA)")
    print("COMO FUNCIONA:")
    print("  1. Analiza historico de prestamos de usuarios")
    print("  2. Identifica usuarios con patrones similares")
    print("  3. Sugiere recursos que usuarios similares pidieron")
    print()
    print("EJEMPLO:")
    print("  Si Usuario A pidio: [Libro Python, Libro Java, Revista Tech]")
    print("  Y Usuario B pidio: [Libro Python, Libro Java, Libro C++]")
    print("  -> Sistema recomienda a A: 'Libro C++ (usuarios similares lo pidieron)'")
    print()
    print("BENEFICIO: Personalizacion como Netflix, Spotify, Amazon")
    print()

    pausa()


def demo_calificaciones(sistema):
    """Demostracion de calificaciones y reviews."""
    limpiar_pantalla()
    print("  CALIFICACIONES Y REVIEWS (COMMUNITY-DRIVEN)")
    print()
    print("COMO FUNCIONA:")
    print("  1. Usuarios califican recursos (1-5 estrellas)")
    print("  2. Escriben comentarios y feedback")
    print("  3. Sistema genera RANKING de mejores recursos")
    print("  4. Comunidad vota utilidad de cada review")
    print()
    print("EJEMPLO:")
    print("  Libro Python (R001):")
    print("    ⭐⭐⭐⭐⭐ 'Excelente, muy didactico' (123 usuarios lo marcaron util)")
    print("    ⭐⭐⭐⭐   'Bueno pero un poco denso' (45 usuarios)")
    print("    Promedio: 4.3/5 estrellas")
    print()
    print("RANKING GENERAL:")
    print("  1. Sala Estudio (R003): 4.9/5 (8 reviews)")
    print("  2. Libro Python (R001): 4.3/5 (3 reviews)")
    print()
    print("BENEFICIO: Como Airbnb, Uber, Amazon - Reviews confiables")
    print()

    pausa()


def demo_prediccion(sistema):
    """Demostracion de prediccion de disponibilidad."""
    limpiar_pantalla()
    print("  PREDICCION DE DISPONIBILIDAD (ANALYTICS)")
    print()
    print("COMO FUNCIONA:")
    print("  1. Registra duracion historica de cada prestamo")
    print("  2. Calcula promedio de dias para cada tipo de recurso")
    print("  3. Analiza patrones de demanda por hora del dia")
    print("  4. Sugiere mejor horario para pedir (menos congestión)")
    print()
    print("EJEMPLO:")
    print("  Usuario pregunta: '¿Cuando estara disponible Libro Python?'")
    print()
    print("  Sistema responde:")
    print("    'Disponible en ~3 dias (78% confianza)'")
    print("    'Mejor horario: 09:00 (menos congestión)'")
    print()
    print("ANALISIS:")
    print("  - Duracion promedio de prestamo: 3.25 dias")
    print("  - Pico de demanda: 14:00 (8 solicitudes)")
    print("  - Mejor horario: 09:00 (2 solicitudes)")
    print()
    print("BENEFICIO: Como Uber (ETA), Amazon (Delivery)")
    print()

    pausa()


def demo_gamificacion(sistema):
    """Demostracion de gamificacion."""
    limpiar_pantalla()
    print("  GAMIFICACION (ENGAGEMENT)")
    print()
    print("COMPONENTES:")
    print()
    print("1. PUNTOS:")
    print("   - Prestamo registrado: +10 puntos")
    print("   - Devolucion a tiempo: +20 puntos")
    print("   - Review escrita: +15 puntos")
    print("   - Busqueda realizada: +2 puntos")
    print()
    print("2. NIVELES (1-10):")
    print("   Nivel 1 Novato (0 pts)   -> Nivel 5 Expert (1000 pts)")
    print("   Nivel 2 Aprendiz (100)  -> Nivel 6 Pro (1500)")
    print("   Nivel 3 Usuario (250)   -> Nivel 10 Supremo (5000)")
    print()
    print("3. BADGES (6 tipos desbloqueables):")
    print("   LEAL: 10+ prestamos")
    print("   DEVOLVEDOR: 5+ devoluciones a tiempo")
    print("   EXPLORADOR: 3+ tipos de recursos")
    print("   CRITICO: 5+ reviews")
    print("   DETECTIVE: 20+ busquedas")
    print("   VIP: Reputacion 4.5+ estrellas")
    print()
    print("4. LEADERBOARDS:")
    print("   - Top usuarios globales por puntos")
    print("   - Usuarios agrupados por nivel")
    print("   - Usuarios con cada badge")
    print()
    print("BENEFICIO: Como LinkedIn, Duolingo, Xbox - Usuario vuelve")
    print()

    pausa()


def gestion_usuarios(gestor):
    """Submenu para gestion de usuarios."""
    limpiar_pantalla()
    print("  GESTION DE USUARIOS (M01)")
    print()

    while True:
        print("\n1. Registrar usuario")
        print("2. Listar usuarios")
        print("3. Consultar usuario")
        print("0. Volver")
        print()

        try:
            opcion = input("Selecciona opcion: ").strip()
        except EOFError:
            break

        if opcion == "0":
            break

        elif opcion == "1":
            nombre = input("\nNombre: ")
            email = input("Email: ")
            # registrar() lanza ValueError si nombre o email están vacíos;
            # sin el try el programa se cerraba con un Traceback.
            try:
                codigo = gestor.registrar(nombre, email)
                print(f"\n Usuario registrado: {codigo}")
            except ValueError as e:
                print(f"\n Error: {e}")

        elif opcion == "2":
            usuarios = gestor.listar_todos()
            print(f"\nTotal usuarios: {len(usuarios)}\n")
            for u in usuarios:
                estado = " Activo" if u.estado == "Activo" else " Inactivo"
                print(f"  {u.codigo}: {u.nombre} ({u.email}) [{estado}]")

        elif opcion == "3":
            codigo = input("\nCodigo usuario: ")
            usuario = gestor.buscar_por_codigo(codigo)
            if usuario:
                print(f"\n  {usuario.codigo}: {usuario.nombre}")
                print(f"  Email: {usuario.email}")
                print(f"  Estado: {usuario.estado}")
                print(f"  Prestamos: {usuario.cantidad_prestamos}")
            else:
                print(f"\n Usuario {codigo} no encontrado")

        pausa()


def gestion_recursos(gestor):
    """Submenu para gestion de recursos."""
    limpiar_pantalla()
    print("  GESTION DE RECURSOS (M02 - Con HERENCIA)")
    print()

    while True:
        print("\n1. Registrar Libro")
        print("2. Registrar Equipo")
        print("3. Registrar Sala")
        print("4. Listar recursos")
        print("5. Consultar recurso")
        print("0. Volver")
        print()

        try:
            opcion = input("Selecciona opcion: ").strip()
        except EOFError:
            break

        if opcion == "0":
            break

        elif opcion == "1":
            nombre = input("\nNombre del libro: ")
            autor = input("Autor: ")
            isbn = input("ISBN: ")
            ano = input("Ano publicacion: ")
            try:
                codigo = gestor.registrar_libro(nombre, autor, isbn, int(ano))
                print(f"\n Libro registrado: {codigo}")
            except ValueError:
                print(f"\n Error: El año debe ser un número válido")

        elif opcion == "2":
            nombre = input("\nNombre equipo: ")
            tipo = input("Tipo de equipo: ")
            modelo = input("Modelo: ")
            ubicacion = input("Ubicacion: ")
            codigo = gestor.registrar_equipo(nombre, tipo, modelo, ubicacion)
            print(f"\n Equipo registrado: {codigo}")

        elif opcion == "3":
            nombre = input("\nNombre sala: ")
            capacidad = input("Capacidad: ")
            try:
                codigo = gestor.registrar_sala(nombre, int(capacidad))
                print(f"\n Sala registrada: {codigo}")
            except ValueError:
                print(f"\n Error: La capacidad debe ser un número válido")

        elif opcion == "4":
            recursos = gestor.listar_todos()
            print(f"\nTotal recursos: {len(recursos)}\n")
            for r in recursos:
                print(f"  {r.codigo}: {r.nombre} ({r.obtener_tipo()})")

        elif opcion == "5":
            codigo = input("\nCodigo recurso: ")
            recurso = gestor.buscar_por_codigo(codigo)
            if recurso:
                print(f"\n  {recurso.codigo}: {recurso.nombre}")
                print(f"  Tipo: {recurso.obtener_tipo()}")
                print(f"  Disponible: {recurso.es_disponible()}")
            else:
                print(f"\n Recurso {codigo} no encontrado")

        pausa()


def solicitar_turno_menu(gestor_turnos, usuario_cod, recurso_cod, sede):
    """Pide turno y muestra la posición. Lo usan los menús de Turnos y de Préstamos."""
    try:
        codigo = gestor_turnos.solicitar_turno(usuario_cod, recurso_cod, sede)
        # La solicitud entra al final, así que su posición es el tamaño de la fila
        posicion = gestor_turnos.obtener_cantidad_espera(recurso_cod)
        print(f"\n Turno {codigo} asignado, posicion {posicion} en la fila")
    except ValueError as e:
        print(f"\n Error: {e}")


def gestion_prestamos(gestor_prestamos, gestor_usuarios, gestor_recursos):
    """Submenu para gestion de prestamos."""
    limpiar_pantalla()
    print("  GESTION DE PRESTAMOS (M03)")
    print()

    while True:
        print("\n1. Registrar prestamo")
        print("2. Registrar devolucion")
        print("3. Listar prestamos activos")
        print("4. Listar prestamos atrasados")
        print("5. Listar prestamos por usuario")
        print("6. Listar prestamos por sede")
        print("7. Consultar prestamo")
        print("8. Deshacer ultima operacion (Pila)")
        print("0. Volver")
        print()

        try:
            opcion = input("Selecciona opcion: ").strip()
        except EOFError:
            break

        if opcion == "0":
            break

        elif opcion == "1":
            usuario_cod = input("\nCodigo usuario: ")
            recurso_cod = input("Codigo recurso: ")
            sede = input("Sede (Centro/Norte/Sur): ")
            try:
                codigo_prestamo = gestor_prestamos.registrar_prestamo(usuario_cod, recurso_cod, sede)
                print(f"\n Prestamo registrado: {codigo_prestamo}")
            except SinUnidadesError as e:
                # Sin unidades en esa sede: se ofrece entrar a la fila de espera (RF3).
                # Va antes de "except ValueError" porque SinUnidadesError es un ValueError.
                print(f"\n Error: {e}")
                if gestor_prestamos.gestor_turnos is not None:
                    try:
                        respuesta = input("¿Desea pedir turno en la fila de espera? (s/n): ")
                    except EOFError:
                        respuesta = "n"
                    if respuesta.strip().lower() == "s":
                        solicitar_turno_menu(gestor_prestamos.gestor_turnos,
                                             usuario_cod, recurso_cod, sede)
            except ValueError as e:
                print(f"\n Error: {e}")

        elif opcion == "2":
            codigo_prestamo = input("\nCodigo prestamo: ")
            try:
                resultado = gestor_prestamos.registrar_devolucion(codigo_prestamo)
                # registrar_devolucion indica el fallo devolviendo False (no lanza
                # error); antes no se revisaba y siempre decía "registrada".
                if not resultado:
                    print(f"\n Error: El prestamo {codigo_prestamo} no existe o ya fue devuelto")
                else:
                    print(f"\n Devolucion registrada")
                    # Si devuelve un código, la unidad pasó al siguiente de la fila
                    if isinstance(resultado, str):
                        asignado = gestor_prestamos.buscar_prestamo(resultado)
                        print(f" Asignado automaticamente a {asignado.usuario_codigo} "
                              f"(siguiente en la fila): {resultado}")
            except ValueError as e:
                print(f"\n Error: {e}")

        elif opcion == "3":
            # listar_activos devuelve un VectorDinamico (no una list)
            activos = gestor_prestamos.listar_activos()
            print(f"\nTotal prestamos activos: {activos.obtener_tamaño()}\n")
            for i in range(activos.obtener_tamaño()):
                p = activos.obtener(i)
                print(f"  {p.codigo}: {p.usuario_codigo} -> {p.recurso_codigo} [{p.sede}]")

        elif opcion == "4":
            prestamos = gestor_prestamos.obtener_prestamos_atrasados()
            print(f"\nTotal prestamos ATRASADOS: {len(prestamos)}\n")
            for p in prestamos:
                dias_atraso = p.dias_atraso()
                print(f"  {p.codigo}: {p.usuario_codigo} -> {p.recurso_codigo} [{dias_atraso} días atraso]")

        elif opcion == "5":
            usuario_cod = input("\nCodigo usuario: ")
            prestamos = gestor_prestamos.obtener_prestamos_usuario(usuario_cod)
            print(f"\nPrestamos de {usuario_cod}: {len(prestamos)}\n")
            for p in prestamos:
                print(f"  {p.codigo}: {p.recurso_codigo} [{p.estado}]")

        elif opcion == "6":
            sede = input("\nSede (Centro/Norte/Sur): ")
            prestamos = gestor_prestamos.obtener_prestamos_sede(sede)
            print(f"\nPrestamos en {sede}: {len(prestamos)}\n")
            for p in prestamos:
                print(f"  {p.codigo}: {p.usuario_codigo} -> {p.recurso_codigo}")

        elif opcion == "7":
            codigo = input("\nCodigo prestamo: ")
            prestamo = gestor_prestamos.buscar_prestamo(codigo)
            if prestamo:
                print(f"\n  {prestamo.codigo}: {prestamo.usuario_codigo} -> {prestamo.recurso_codigo}")
                print(f"  Sede: {prestamo.sede}")
                print(f"  Fecha: {prestamo.fecha_prestamo.strftime('%Y-%m-%d %H:%M')}")
                print(f"  Estado: {prestamo.estado}")
                if prestamo.esta_atrasado():
                    print(f"    ATRASADO: {prestamo.dias_atraso()} días")
            else:
                print(f"\n Prestamo {codigo} no encontrado")

        elif opcion == "8":
            # deshacer() puede lanzar ValueError si ya no hay unidad para revertir una devolución
            try:
                if gestor_prestamos.deshacer():
                    print(f"\n Operacion deshecha (Pila LIFO)")
                else:
                    print(f"\n  No hay operaciones para deshacer")
            except ValueError as e:
                print(f"\n Error: {e}")

        pausa()


def gestion_inventario(gestor):
    """Muestra la matriz de inventario."""
    limpiar_pantalla()
    print("  MATRIZ DE INVENTARIO (M02)")
    print()
    print("Disponibilidad por sede y recurso:")
    print()
    print(gestor.inventario.mostrar_matriz())
    pausa()


def gestion_turnos(gestor_turnos):
    """Submenu para gestion de turnos (M04)."""
    limpiar_pantalla()
    print("  GESTION DE TURNOS (M04 - Cola FIFO)")
    print()

    while True:
        print("\n1. Ver siguiente turno")
        print("2. Ver fila de espera (por recurso)")
        print("3. Ver cantidad en espera")
        print("4. Solicitar turno")
        print("0. Volver")
        print()

        try:
            opcion = input("Selecciona opcion: ").strip()
        except EOFError:
            break

        if opcion == "0":
            break
        elif opcion == "1":
            recurso = input("\nCodigo recurso: ")
            # ver_siguiente solo consulta; obtener_siguiente sacaba al usuario de la fila
            siguiente = gestor_turnos.ver_siguiente(recurso)
            if siguiente:
                print(f"\n Siguiente en fila: {siguiente.usuario_codigo} (turno {siguiente.codigo})")
            else:
                print(f"\n  No hay nadie en fila para {recurso}")
        elif opcion == "2":
            recurso = input("\nCodigo recurso: ")
            fila = gestor_turnos.obtener_fila(recurso)
            print(f"\nFila para {recurso}: {len(fila)} personas\n")
            for i, sol in enumerate(fila, 1):
                print(f"  {i}. {sol.usuario_codigo}")
        elif opcion == "3":
            recurso = input("\nCodigo recurso: ")
            cantidad = gestor_turnos.obtener_cantidad_espera(recurso)
            print(f"\n{cantidad} personas esperando por {recurso}")
        elif opcion == "4":
            # Antes no había forma de entrar a la fila desde el programa (RF3)
            usuario_cod = input("\nCodigo usuario: ")
            recurso_cod = input("Codigo recurso: ")
            sede = input("Sede (Centro/Norte/Sur): ")
            solicitar_turno_menu(gestor_turnos, usuario_cod, recurso_cod, sede)

        pausa()


def gestion_categorias(gestor_categorias):
    """Submenu para gestion de categorias (M05 - Árbol)."""
    limpiar_pantalla()
    print("  GESTION DE CATEGORIAS (M05 - Árbol Binario)")
    print()

    while True:
        print("\n1. Registrar categoria")
        print("2. Buscar categoria")
        print("3. Listar todas las categorias")
        print("0. Volver")
        print()

        try:
            opcion = input("Selecciona opcion: ").strip()
        except EOFError:
            break

        if opcion == "0":
            break
        elif opcion == "1":
            codigo = input("\nCodigo categoria: ")
            nombre = input("Nombre categoria: ")
            # registrar_categoria lanza ValueError si el código ya existe (RF7)
            try:
                gestor_categorias.registrar_categoria(codigo, nombre)
                print(f"\n Categoria registrada: {codigo}")
            except ValueError as e:
                print(f"\n Error: {e}")
        elif opcion == "2":
            codigo = input("\nCodigo categoria: ")
            cat = gestor_categorias.obtener_categoria(codigo)
            if cat:
                print(f"\n  {cat.codigo}: {cat.nombre}")
            else:
                print(f"\n  Categoria {codigo} no encontrada")
        elif opcion == "3":
            cantidad = gestor_categorias.obtener_cantidad()
            print(f"\nTotal categorias: {cantidad}")

        pausa()


def gestion_informes(generador):
    """Submenu para informes y reportes (M06)."""
    limpiar_pantalla()
    print("  INFORMES Y REPORTES (M06)")
    print()

    while True:
        print("\n1. Reporte de uso (prestamos)")
        print("2. Reporte de inventario")
        print("0. Volver")
        print()

        try:
            opcion = input("Selecciona opcion: ").strip()
        except EOFError:
            break

        if opcion == "0":
            break
        elif opcion == "1":
            print("\n REPORTE DE USO:")
            print(generador.generar_reporte_uso())
        elif opcion == "2":
            print("\n REPORTE DE INVENTARIO:")
            print(generador.generar_reporte_inventario())

        pausa()


def pruebas_estructuras():
    """Demostracion de estructuras de datos."""
    limpiar_pantalla()
    print("  PRUEBAS DE ESTRUCTURAS DE DATOS (8 propias)")
    print()

    print("1. VECTOR DINAMICO (O(1) amortizado):")
    v = VectorDinamico(capacidad_inicial=2)
    v.agregar("A")
    v.agregar("B")
    print(f"   Despues agregar A, B: tamaño={v.obtener_tamaño()}, capacidad={v.obtener_capacidad()}")
    v.agregar("C")
    print(f"   Despues agregar C: tamaño={v.obtener_tamaño()}, capacidad={v.obtener_capacidad()}")
    print(f"   Contenido: {[v.obtener(i) for i in range(v.obtener_tamaño())]}")
    print()

    print("2. LISTA SIMPLE (O(n) busqueda, O(1) insercion):")
    ls = ListaSimple()
    ls.agregar_al_final("X")
    ls.agregar_al_final("Y")
    ls.agregar_al_final("Z")
    print(f"   Contenido: {ls.recorrer()}")
    print()

    print("3. LISTA DOBLE (Bidireccional):")
    ld = ListaDoble()
    ld.agregar_al_final(1)
    ld.agregar_al_final(2)
    ld.agregar_al_final(3)
    print(f"   Adelante: {ld.recorrer_adelante()}")
    print(f"   Atras:    {ld.recorrer_atras()}")
    print()

    print("4. PILA - LIFO (O(1) push/pop):")
    p = Pila()
    p.push("Op1")
    p.push("Op2")
    p.push("Op3")
    print(f"   Tope: {p.peek()}")
    print(f"   Pop: {p.pop()}, nuevo tope: {p.peek()}")
    print()

    print("5. COLA - FIFO (O(1) encolar/desencolar):")
    c = ColaFIFO()
    c.encolar("User1")
    c.encolar("User2")
    c.encolar("User3")
    print(f"   Frente: {c.frente()}")
    print(f"   Desencolar: {c.desencolar()}, nuevo frente: {c.frente()}")
    print()

    print(" Todas las estructuras funcionan correctamente")
    print()

    pausa()


def main():
    """Funcion principal."""
    print("Cargando sistema...")

    # Crear gestores (M01-M08)
    gestor_usuarios = GestorUsuarios()
    gestor_recursos = GestorRecursos(num_sedes=3)
    # GestorTurnos recibe usuarios y recursos para validar "Solicitar turno"
    gestor_turnos = GestorTurnos(
        gestor_usuarios=gestor_usuarios,
        gestor_recursos=gestor_recursos
    )
    gestor_prestamos = GestorPrestamos(
        gestor_turnos=gestor_turnos,
        gestor_usuarios=gestor_usuarios,
        gestor_recursos=gestor_recursos
    )
    gestor_categorias = GestorCategorias()
    # Argumentos con nombre: antes se pasaba (gestor_usuarios, gestor_recursos) por
    # posición y el reporte de uso contaba recursos y el de inventario mostraba usuarios.
    generador_informes = GeneradorInformes(
        gestor_recursos=gestor_recursos,
        gestor_prestamos=gestor_prestamos
    )
    sistema_inteligente = SistemaInteligente()

    # Pre-cargar datos
    print("Cargando datos de ejemplo...")

    cod_u1 = gestor_usuarios.registrar("Carlos Lopez", "carlos@uni.edu")
    cod_u2 = gestor_usuarios.registrar("Ana Garcia", "ana@uni.edu")

    gestor_recursos.registrar_sede(0, "Centro")
    gestor_recursos.registrar_sede(1, "Norte")
    gestor_recursos.registrar_sede(2, "Sur")

    cod_r1 = gestor_recursos.registrar_libro("Python 101", "Guido van Rossum", "978-123", 2020)
    cod_r2 = gestor_recursos.registrar_equipo("Proyector 1", "Proyector", "Epson", "Sala A")
    cod_r3 = gestor_recursos.registrar_sala("Sala de Estudio", 30)

    gestor_recursos.actualizar_disponibilidad(cod_r1, "Centro", 5)
    gestor_recursos.actualizar_disponibilidad(cod_r2, "Centro", 2)
    gestor_recursos.actualizar_disponibilidad(cod_r3, "Centro", 1)

    print(" Sistema listo\n")

    # Menu interactivo
    while True:
        menu_principal()

        try:
            opcion = input("Selecciona opcion: ").strip()
        except EOFError:
            break

        if opcion == "0":
            print("\n¡Hasta luego! \n")
            break

        elif opcion == "1":
            gestion_usuarios(gestor_usuarios)

        elif opcion == "2":
            gestion_recursos(gestor_recursos)

        elif opcion == "3":
            gestion_inventario(gestor_recursos)

        elif opcion == "4":
            gestion_prestamos(gestor_prestamos, gestor_usuarios, gestor_recursos)

        elif opcion == "5":
            gestion_turnos(gestor_turnos)

        elif opcion == "6":
            gestion_categorias(gestor_categorias)

        elif opcion == "7":
            gestion_informes(generador_informes)

        elif opcion == "8":
            pruebas_estructuras()

        elif opcion == "9":
            menu_funciones_inteligentes(sistema_inteligente)

        else:
            print("\n Opcion invalida")
            pausa()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n¡Programa interrumpido! \n")
        sys.exit(0)
