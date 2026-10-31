"""Gestor de Turnos (Solicitudes) — M04"""
from estructuras import ColaFIFO, TablaHash
from .solicitud import Solicitud


class GestorTurnos:
    """Gestiona solicitudes de turnos respetando orden FIFO."""

    def __init__(self, gestor_usuarios=None, gestor_recursos=None):
        """
        gestor_usuarios: GestorUsuarios (M01) opcional, para validar al solicitar turno.
        gestor_recursos: GestorRecursos (M02) opcional, para validar recurso, sede e inventario.

        Se reciben igual que en GestorPrestamos (opcionales), así GestorTurnos()
        sin argumentos sigue funcionando.
        """
        self.colas = TablaHash(211)  # {recurso_codigo: ColaFIFO de Solicitudes}
        self.solicitudes = TablaHash(211)  # {codigo_solicitud: Solicitud}
        self.contador = 0
        self.gestor_usuarios = gestor_usuarios
        self.gestor_recursos = gestor_recursos

    @staticmethod
    def _par(usuario_codigo, recurso_codigo):
        """Clave para verificar si un usuario está esperando un recurso."""
        return f"{usuario_codigo}|{recurso_codigo}"

    def encolar(self, usuario_codigo, recurso_codigo):
        """Agrega usuario a cola de espera para un recurso. O(1) amortizado."""
        cola = self.colas.buscar(recurso_codigo)
        if cola is None:
            cola = ColaFIFO()
            self.colas.insertar(recurso_codigo, cola)

        self.contador += 1
        codigo = f"S{self.contador:04d}"
        solicitud = Solicitud(codigo, usuario_codigo, recurso_codigo)
        cola.encolar(solicitud)
        self.solicitudes.insertar(codigo, solicitud)
        return codigo

    def esta_en_espera(self, usuario_codigo, recurso_codigo):
        """¿El usuario ya tiene turno en la fila de ese recurso? O(n), n = tamaño de la fila."""
        cola = self.colas.buscar(recurso_codigo)
        if cola is None:
            return False
        for sol in cola.recorrer():
            if sol.usuario_codigo == usuario_codigo:
                return True
        return False

    def solicitar_turno(self, usuario_codigo, recurso_codigo, sede):
        """
        Pide turno en la fila de espera de un recurso (RF3 / RQF-016).

        A diferencia de encolar(), valida los datos antes de entrar a la fila.
        Solo se puede pedir turno si la sede NO tiene unidades: si las tiene,
        lo correcto es registrar el préstamo directamente.

        Returns:
            str: código de la solicitud (ej: "S0001"). Como entra al final, su
                 posición en la fila es obtener_cantidad_espera(recurso_codigo).

        Raises:
            ValueError: usuario inexistente o inactivo, recurso inexistente o
                        dado de baja, sede inexistente, hay unidades disponibles,
                        o el usuario ya está en la fila de ese recurso.

        Complejidad: O(n) por la verificación de duplicados (n = personas en la fila).
        """
        if self.gestor_usuarios:
            usuario = self.gestor_usuarios.buscar_por_codigo(usuario_codigo)
            if usuario is None:
                raise ValueError(f"Usuario {usuario_codigo} no existe")
            if not usuario.es_activo():
                raise ValueError(f"El usuario {usuario_codigo} esta inactivo")

        if self.gestor_recursos:
            recurso = self.gestor_recursos.buscar_por_codigo(recurso_codigo)
            if recurso is None:
                raise ValueError(f"Recurso {recurso_codigo} no existe")
            if recurso.obtener_estado() == "Dado de baja":
                raise ValueError(f"El recurso {recurso_codigo} esta dado de baja")
            # Misma validación de sede que GestorPrestamos.registrar_prestamo
            sede_existe = any(s.nombre == sede for s in self.gestor_recursos.listar_sedes())
            if not sede_existe:
                raise ValueError(f"Sede '{sede}' no existe")
            # La fila es para cuando no hay unidades (RQF-016); con unidades se presta.
            if self.gestor_recursos.obtener_disponibilidad(recurso_codigo, sede) > 0:
                raise ValueError("Hay unidades disponibles: registre el préstamo")

        if self.esta_en_espera(usuario_codigo, recurso_codigo):
            raise ValueError(f"El usuario {usuario_codigo} ya esta en la fila de {recurso_codigo}")

        return self.encolar(usuario_codigo, recurso_codigo)

    def ver_siguiente(self, recurso_codigo):
        """
        Consulta quién sigue en la fila SIN sacarlo. O(1).

        obtener_siguiente() desencola y marca la solicitud como "Otorgado"; si el
        menú lo usa solo para mirar, el usuario pierde su turno. Por eso aquí se
        usa ColaFIFO.frente(), que no modifica la cola.
        """
        cola = self.colas.buscar(recurso_codigo)
        if cola is None:
            return None
        return cola.frente()

    def obtener_siguiente(self, recurso_codigo):
        """
        Saca (desencola) la siguiente solicitud y la marca "Otorgado". O(1).

        Solo debe usarse al asignar el recurso; para consultar usar ver_siguiente().
        """
        cola = self.colas.buscar(recurso_codigo)
        if cola is None or cola.esta_vacia():
            return None

        solicitud = cola.desencolar()
        if solicitud is not None:
            solicitud.otorgar()
        return solicitud

    def obtener_fila(self, recurso_codigo):
        """Obtiene todas las solicitudes en espera para un recurso. O(n)."""
        cola = self.colas.buscar(recurso_codigo)
        if cola is None:
            return []
        return cola.recorrer()

    def obtener_cantidad_espera(self, recurso_codigo):
        """Obtiene cantidad de solicitudes en espera para un recurso. O(1)."""
        cola = self.colas.buscar(recurso_codigo)
        if cola is None:
            return 0
        return cola.obtener_tamaño()

    def cancelar_solicitud(self, codigo_solicitud):
        """Cancela una solicitud. O(n) en peor caso."""
        solicitud = self.solicitudes.buscar(codigo_solicitud)
        if solicitud is None or solicitud.estado != "En espera":
            return False

        # Reconstruir la cola sin esta solicitud
        cola = self.colas.buscar(solicitud.recurso_codigo)
        if cola is not None:
            nueva_cola = ColaFIFO()
            for sol in cola.recorrer():
                if sol.codigo != codigo_solicitud:
                    nueva_cola.encolar(sol)
            self.colas.insertar(solicitud.recurso_codigo, nueva_cola)

        solicitud.cancelar()
        return True

    def reinsertar_al_frente(self, solicitud):
        """Devuelve una solicitud otorgada al primer lugar de su fila."""
        cola = self.colas.buscar(solicitud.recurso_codigo)
        if cola is None:
            cola = ColaFIFO()

        nueva_cola = ColaFIFO()
        nueva_cola.encolar(solicitud)
        for sol in (cola.recorrer() if cola is not None else []):
            if sol.codigo != solicitud.codigo:
                nueva_cola.encolar(sol)

        self.colas.insertar(solicitud.recurso_codigo, nueva_cola)
        solicitud.reiniciar()

    def obtener_cantidad(self):
        """Obtiene cantidad total de solicitudes en espera. O(V * E) donde V=colas, E=promedio por cola."""
        total = 0
        for recurso_codigo in self.colas.obtener_todas_las_claves():
            cola = self.colas.buscar(recurso_codigo)
            if cola is not None:
                total += cola.obtener_tamaño()
        return total

    def buscar_solicitud(self, codigo):
        """Busca una solicitud por código. O(1) promedio."""
        return self.solicitudes.buscar(codigo)

    def __str__(self):
        cantidad = self.obtener_cantidad()
        return f"GestorTurnos(colas={len(self.colas.obtener_todas_las_claves())}, en_espera={cantidad})"
