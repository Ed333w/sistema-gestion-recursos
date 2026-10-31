"""Reproduce E9, E10 y E11 (uso: python repro_e9_e11.py <carpeta_proyecto>)."""
import sys, io
sys.path.insert(0, sys.argv[1])
from modulos import GestorUsuarios, GestorRecursos, GestorTurnos, GestorPrestamos

# E10: 500 recursos con existencias
gu = GestorUsuarios(); gr = GestorRecursos(num_sedes=3); gr.registrar_sede(0, "Centro")
try:
    for i in range(500):
        c = gr.registrar_libro(f"L{i}", "a", "i", 2000)
        gr.actualizar_disponibilidad(c, "Centro", 3)
    print("E10: 500 recursos OK; R0500 =", gr.obtener_disponibilidad("R0500", "Centro"))
except ValueError as e:
    print(f"E10: ValueError en el recurso {gr.obtener_cantidad()} ({c}): {e}")
    print(f"     {c} registrado en GestorRecursos: {gr.buscar_por_codigo(c) is not None}; "
          f"disponibilidad en la matriz: {gr.obtener_disponibilidad(c, 'Centro')}")

# E9: préstamo a usuario inactivo
gu = GestorUsuarios(); gr = GestorRecursos(num_sedes=3); gr.registrar_sede(0, "Centro")
gt = GestorTurnos(); gp = GestorPrestamos(gestor_turnos=gt, gestor_usuarios=gu, gestor_recursos=gr)
u1 = gu.registrar("Carlos", "c@u"); r1 = gr.registrar_libro("Py", "a", "i", 2020)
gr.actualizar_disponibilidad(r1, "Centro", 5)
gu.dar_de_baja(u1)
try:
    print("E9: préstamo a usuario INACTIVO ->", gp.registrar_prestamo(u1, r1, "Centro"))
except ValueError as e:
    print("E9: rechazado:", e)
r2 = gr.registrar_libro("Baja", "a", "i", 2020); gr.actualizar_disponibilidad(r2, "Centro", 1)
gr.dar_de_baja(r2); u2 = gu.registrar("Ana", "a@u")
try:
    print("E9: préstamo de recurso DADO DE BAJA ->", gp.registrar_prestamo(u2, r2, "Centro"))
except ValueError as e:
    print("E9: rechazado:", e)

# E11: encolar U002 y U003 en un recurso, atender_siguiente_turno, deshacer
gu = GestorUsuarios(); gr = GestorRecursos(num_sedes=3); gr.registrar_sede(0, "Centro")
gt = GestorTurnos(); gp = GestorPrestamos(gestor_turnos=gt, gestor_usuarios=gu, gestor_recursos=gr)
for n in ("A", "B", "C"):
    gu.registrar(n, n + "@u")
for i in range(5):
    gr.registrar_libro(f"L{i}", "a", "i", 2000)
gr.actualizar_disponibilidad("R0005", "Centro", 1)
gt.encolar("U002", "R0005"); gt.encolar("U003", "R0005")
print("E11: cola antes  =", [s.usuario_codigo for s in gt.obtener_fila("R0005")])
cod = gp.atender_siguiente_turno("R0005", "Centro")
print("E11: atendido    =", cod, "| cola =", [s.usuario_codigo for s in gt.obtener_fila("R0005")])
gp.deshacer()
print("E11: tras deshacer cola =", [s.usuario_codigo for s in gt.obtener_fila("R0005")],
      "| estado S0001 =", gt.buscar_solicitud("S0001").estado)
