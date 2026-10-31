"""
SISTEMA INTELIGENTE — Clase Principal de M08 (Carpeta: M09_sistema_inteligente para compatibilidad)

Integra todas las características innovadoras de startup:
1. Recomendaciones inteligentes (IA)
2. Calificaciones y reviews (Community)
3. Predicción de disponibilidad (Analytics)
4. Gamificación (Badges, Puntos, Leaderboards)
"""

from estructuras import VectorDinamico
from datetime import datetime, timedelta


class SistemaInteligente:
    """
    Sistema integrado de features innovadoras.

    COMPONENTES:
    ├─ Recomendaciones: Collaborative Filtering
    ├─ Calificaciones: Reviews 1-5 estrellas
    ├─ Predicción: Forecast de disponibilidad
    └─ Gamificación: Puntos, Badges, Niveles
    """

    def __init__(self):
        """Inicializa el sistema inteligente."""
        # Recomendaciones
        self.historial_prestamos = VectorDinamico()
        self.recomendaciones_cache = {}

        # Calificaciones
        self.calificaciones = VectorDinamico()

        # Predicción
        self.duraciones_promedio = {}
        self.demanda_por_hora = {}

        # Gamificación
        self.usuarios_gamificados = {}

    def registrar_prestamo_hist(self, usuario_codigo, recurso_codigo):
        """Registra préstamo para análisis de recomendaciones."""
        self.historial_prestamos.agregar((usuario_codigo, recurso_codigo, datetime.now()))
        if usuario_codigo in self.recomendaciones_cache:
            del self.recomendaciones_cache[usuario_codigo]

    def recomendar_recursos(self, usuario_codigo, top_n=5):
        """Recomienda recursos basado en Collaborative Filtering."""
        recursos_usuario = set()
        for i in range(self.historial_prestamos.obtener_tamaño()):
            user, recurso, _ = self.historial_prestamos.obtener(i)
            if user == usuario_codigo:
                recursos_usuario.add(recurso)

        usuarios_unicos = set()
        for i in range(self.historial_prestamos.obtener_tamaño()):
            user, _, _ = self.historial_prestamos.obtener(i)
            usuarios_unicos.add(user)

        recursos_sugeridos = {}
        for otro_usuario in usuarios_unicos:
            if otro_usuario == usuario_codigo:
                continue

            recursos_otro = set()
            for i in range(self.historial_prestamos.obtener_tamaño()):
                user, recurso, _ = self.historial_prestamos.obtener(i)
                if user == otro_usuario:
                    recursos_otro.add(recurso)

            interseccion = len(recursos_usuario & recursos_otro)
            union = len(recursos_usuario | recursos_otro)
            similitud = interseccion / union if union > 0 else 0.0

            for recurso in recursos_otro:
                if recurso not in recursos_usuario:
                    if recurso not in recursos_sugeridos:
                        recursos_sugeridos[recurso] = 0
                    recursos_sugeridos[recurso] += similitud

        recomendaciones = [(r, s, "Usuarios similares lo pidieron")
                          for r, s in recursos_sugeridos.items()]
        recomendaciones.sort(key=lambda x: x[1], reverse=True)
        return recomendaciones[:top_n]

    def registrar_calificacion(self, usuario_codigo, recurso_codigo, estrellas, comentario=""):
        """Registra una calificación (1-5 estrellas)."""
        if not 1 <= estrellas <= 5:
            raise ValueError("Estrellas deben estar entre 1 y 5")

        self.calificaciones.agregar({
            'usuario': usuario_codigo,
            'recurso': recurso_codigo,
            'estrellas': estrellas,
            'comentario': comentario,
            'fecha': datetime.now()
        })

    def obtener_promedio_recurso(self, recurso_codigo):
        """Obtiene promedio de estrellas para un recurso."""
        suma = 0
        cantidad = 0

        for i in range(self.calificaciones.obtener_tamaño()):
            cal = self.calificaciones.obtener(i)
            if cal['recurso'] == recurso_codigo:
                suma += cal['estrellas']
                cantidad += 1

        return suma / cantidad if cantidad > 0 else 0.0

    def ranking_recursos(self, top_n=10):
        """Ranking de mejores recursos por calificación."""
        recursos = {}

        for i in range(self.calificaciones.obtener_tamaño()):
            cal = self.calificaciones.obtener(i)
            recurso = cal['recurso']
            if recurso not in recursos:
                recursos[recurso] = []
            recursos[recurso].append(cal['estrellas'])

        ranking = []
        for recurso, estrellas_list in recursos.items():
            promedio = sum(estrellas_list) / len(estrellas_list)
            ranking.append((recurso, promedio, len(estrellas_list)))

        ranking.sort(key=lambda x: (x[1], x[2]), reverse=True)
        return ranking[:top_n]

    def registrar_prestamo_finalizado(self, recurso_codigo, fecha_inicio, fecha_fin):
        """Registra préstamo completado para predicción."""
        duracion = (fecha_fin - fecha_inicio).days
        if duracion < 0:
            duracion = 0

        if recurso_codigo not in self.duraciones_promedio:
            self.duraciones_promedio[recurso_codigo] = []
        self.duraciones_promedio[recurso_codigo].append(duracion)

        hora = fecha_inicio.hour
        self.demanda_por_hora[hora] = self.demanda_por_hora.get(hora, 0) + 1

    def predecir_disponibilidad(self, recurso_codigo):
        """Predice cuándo estará disponible un recurso."""
        if recurso_codigo not in self.duraciones_promedio:
            duracion_prom = 3.0
            confianza = 0.0
        else:
            duraciones = self.duraciones_promedio[recurso_codigo]
            duracion_prom = sum(duraciones) / len(duraciones)
            confianza = min(len(duraciones) / 10.0, 1.0)

        fecha_estimada = datetime.now() + timedelta(days=duracion_prom)

        return {
            'fecha_estimada': fecha_estimada,
            'dias_estimados': int(duracion_prom),
            'confianza': confianza,
            'mensaje': f"Disponible en ~{int(duracion_prom)} días ({int(confianza*100)}% confianza)"
        }

    def crear_usuario_gamificado(self, usuario_codigo):
        """Inicializa usuario con sistema de gamificación."""
        self.usuarios_gamificados[usuario_codigo] = {
            'puntos': 0,
            'nivel': 1,
            'badges': set(),
            'prestamos': 0,
            'devoluciones_tiempo': 0
        }

    def agregar_puntos(self, usuario_codigo, cantidad):
        """Agrega puntos a usuario y actualiza nivel."""
        if usuario_codigo not in self.usuarios_gamificados:
            self.crear_usuario_gamificado(usuario_codigo)

        usuario = self.usuarios_gamificados[usuario_codigo]
        usuario['puntos'] += cantidad

        puntos_nivel = {1: 0, 2: 100, 3: 250, 4: 500, 5: 1000,
                       6: 1500, 7: 2000, 8: 3000, 9: 4000, 10: 5000}
        for nivel in range(10, 0, -1):
            if usuario['puntos'] >= puntos_nivel[nivel]:
                usuario['nivel'] = nivel
                break

    def registrar_prestamo_gami(self, usuario_codigo):
        """Registra préstamo (gamificación)."""
        if usuario_codigo not in self.usuarios_gamificados:
            self.crear_usuario_gamificado(usuario_codigo)

        usuario = self.usuarios_gamificados[usuario_codigo]
        usuario['prestamos'] += 1
        self.agregar_puntos(usuario_codigo, 10)

        if usuario['prestamos'] >= 10:
            usuario['badges'].add('LEAL')

    def registrar_devolucion_tiempo(self, usuario_codigo):
        """Registra devolución a tiempo (gamificación)."""
        if usuario_codigo not in self.usuarios_gamificados:
            self.crear_usuario_gamificado(usuario_codigo)

        usuario = self.usuarios_gamificados[usuario_codigo]
        usuario['devoluciones_tiempo'] += 1
        self.agregar_puntos(usuario_codigo, 20)

        if usuario['devoluciones_tiempo'] >= 5:
            usuario['badges'].add('DEVOLVEDOR')

    def leaderboard(self, top_n=10):
        """Retorna top N usuarios por puntos."""
        ranking = []
        for user_codigo, data in self.usuarios_gamificados.items():
            ranking.append((user_codigo, data['puntos'], data['nivel']))

        ranking.sort(key=lambda x: x[1], reverse=True)
        return ranking[:top_n]

    def obtener_usuario_gami(self, usuario_codigo):
        """Retorna datos gamificados del usuario."""
        if usuario_codigo not in self.usuarios_gamificados:
            self.crear_usuario_gamificado(usuario_codigo)

        return self.usuarios_gamificados[usuario_codigo]

    def estadisticas(self):
        """Estadísticas globales del sistema."""
        total_usuarios = len(self.usuarios_gamificados)
        if total_usuarios == 0:
            return {
                'total_usuarios': 0,
                'promedio_puntos': 0,
                'promedio_nivel': 0
            }

        suma_puntos = sum(u['puntos'] for u in self.usuarios_gamificados.values())
        suma_niveles = sum(u['nivel'] for u in self.usuarios_gamificados.values())

        return {
            'total_usuarios': total_usuarios,
            'promedio_puntos': suma_puntos / total_usuarios,
            'promedio_nivel': suma_niveles / total_usuarios
        }
