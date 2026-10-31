"""E6b y E6c fuera del menú (uso: python repro_e6bc.py <carpeta_proyecto>)."""
import sys
sys.path.insert(0, sys.argv[1])
from modulos import GestorUsuarios, GestorRecursos, GestorTurnos, GestorPrestamos

gu = GestorUsuarios(); gr = GestorRecursos(num_sedes=3); gr.registrar_sede(0, "Centro")
gt = GestorTurnos(); gp = GestorPrestamos(gestor_turnos=gt, gestor_usuarios=gu, gestor_recursos=gr)
gu.registrar("Carlos", "c@u"); gu.registrar("Ana", "a@u")
gr.registrar_sala("Sala de Estudio", 30); gr.actualizar_disponibilidad("R0001", "Centro", 1)

# E6b: lo que hacía el menú "Ver siguiente turno"
gt.encolar("U002", "R0001")
consulta = gt.ver_siguiente("R0001") if hasattr(gt, "ver_siguiente") else gt.obtener_siguiente("R0001")
print("E6b: 'Ver siguiente' muestra", consulta.usuario_codigo,
      "| personas en fila después de mirar:", gt.obtener_cantidad_espera("R0001"),
      "| estado S0001:", gt.buscar_solicitud("S0001").estado)

# E6c: devolver con alguien en la fila
gt2 = GestorTurnos(); gp2 = GestorPrestamos(gestor_turnos=gt2, gestor_usuarios=gu, gestor_recursos=gr)
p = gp2.registrar_prestamo("U001", "R0001", "Centro")
gt2.encolar("U002", "R0001")
r = gp2.registrar_devolucion(p)
print("E6c: registrar_devolucion devuelve", repr(r),
      "| fila después:", [s.usuario_codigo for s in gt2.obtener_fila("R0001")],
      "| préstamos activos de U002:", len(gp2.obtener_prestamos_usuario("U002")))
