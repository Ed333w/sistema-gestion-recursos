"""Generador de Informes — CLASE PRINCIPAL DE M07

Combina:
- Reportes (fue M09_informes)
- Listados y Ordenamientos (fue M06_listados - INTEGRADO)
"""


class Ordenamientos:
    """Utilidades para ordenamiento de datos."""

    @staticmethod
    def bubble_sort(arr, clave=lambda x: x):
        """Ordena usando bubble sort. O(n²)"""
        arr_copia = arr.copy()
        for i in range(len(arr_copia)):
            for j in range(len(arr_copia)-1-i):
                if clave(arr_copia[j]) > clave(arr_copia[j+1]):
                    arr_copia[j], arr_copia[j+1] = arr_copia[j+1], arr_copia[j]
        return arr_copia

    @staticmethod
    def quick_sort(arr, clave=lambda x: x, izq=0, der=None):
        """Ordena usando quick sort. O(n log n) promedio"""
        if der is None:
            der = len(arr) - 1

        if izq < der:
            p = Ordenamientos._particionar(arr, clave, izq, der)
            Ordenamientos.quick_sort(arr, clave, izq, p - 1)
            Ordenamientos.quick_sort(arr, clave, p + 1, der)
        return arr

    @staticmethod
    def _particionar(arr, clave, izq, der):
        """Particiona para quick sort"""
        pivote = clave(arr[der])
        i = izq - 1
        for j in range(izq, der):
            if clave(arr[j]) < pivote:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[der] = arr[der], arr[i + 1]
        return i + 1


class GeneradorInformes:
    """
    Generador de reportes e informes.
    También incluye funcionalidad de listados y ordenamientos.

    CLASE PRINCIPAL DE M07 (Antes M09_informes, ahora con M06_listados integrado)
    """

    def __init__(self, gestor_recursos=None, gestor_prestamos=None):
        """Inicializa generador con gestores opcionales."""
        self.gestor_recursos = gestor_recursos
        self.gestor_prestamos = gestor_prestamos

    # ─────────────────────────────────────────────────────────
    # REPORTES
    # ─────────────────────────────────────────────────────────

    def generar_reporte_uso(self):
        """Genera reporte de uso de sistema."""
        if not self.gestor_prestamos:
            return "Sin datos"
        total = self.gestor_prestamos.obtener_cantidad()
        return f"Total de préstamos registrados: {total}"

    def generar_reporte_inventario(self):
        """Genera reporte de inventario."""
        if not self.gestor_recursos:
            return "Sin datos"
        return str(self.gestor_recursos)

    # ─────────────────────────────────────────────────────────
    # LISTADOS (Integrados desde M06_listados eliminado)
    # ─────────────────────────────────────────────────────────

    def listar_recursos_ordenados_nombre(self, recursos):
        """Lista recursos ordenados por nombre."""
        return Ordenamientos.bubble_sort(recursos.copy(), lambda r: r.nombre)

    def listar_recursos_ordenados_prestamos(self, recursos):
        """Lista recursos ordenados por cantidad de préstamos."""
        return Ordenamientos.bubble_sort(
            recursos.copy(),
            lambda r: -r.cantidad_prestamos
        )

    def listar_usuarios_ordenados_nombre(self, usuarios):
        """Lista usuarios ordenados por nombre."""
        return Ordenamientos.bubble_sort(usuarios.copy(), lambda u: u.nombre)

    def obtener_ordenamientos(self):
        """Retorna utilidad de ordenamientos para uso directo."""
        return Ordenamientos
