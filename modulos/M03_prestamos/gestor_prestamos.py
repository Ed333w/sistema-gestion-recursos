"""Clase GestorPrestamos — M03 (PRINCIPAL)"""
from estructuras import VectorDinamico, ListaSimple, ListaDoble, Pila, TablaHash
from .prestamo import Prestamo


def _num(codigo):
    """'P0042' -> 42"""
    return int(str(codigo)[1:])


class SinUnidadesError(ValueError):
    """
    No quedan unidades del recurso en la sede pedida.

    Es un ValueError (se captura igual que los demás errores de datos), pero con
    nombre propio para que el menú distinga este caso y ofrezca pedir turno.
    """


class GestorPrestamos:
    """Administra los préstamos del sistema."""

    def __init__(self, gestor_turnos=None, gestor_usuarios=None, gestor_recursos=None):
        """
        gestor_turnos: GestorTurnos (M04) opcional, para integrar turnos.
        gestor_usuarios: GestorUsuarios (M01) opcional, para validar usuarios.
        gestor_recursos: GestorRecursos (M02) opcional, para validar recursos
                         y descontar/sumar unidades en la matriz de inventario.

        Se eliminó el parámetro `exclusivo`: permitía un solo préstamo por recurso
        en todo el sistema. Ahora la disponibilidad la decide el inventario de
        cada sede (RQF-009 / RQF-011).
        """
        self.prestamos = VectorDinamico(capacidad_inicial=50)
        self.historial_simple = ListaSimple()
        self.historial_doble = ListaDoble()
        self.pila_deshacer = Pila()
        self.contador_codigos = 0
        self.gestor_turnos = gestor_turnos
        self.gestor_usuarios = gestor_usuarios
        self.gestor_recursos = gestor_recursos

        # Índices para O(1) promedio en búsquedas
        self.indice_codigo = TablaHash(211)      # código -> Prestamo
        self.recursos_activos = TablaHash(211)   # recurso -> cantidad de activos

    def _indexar_activo(self, p):
        """Indexa un préstamo activo."""
        n = self.recursos_activos.buscar(p.recurso_codigo)
        if n is None:
            n = 0
        self.recursos_activos.insertar(p.recurso_codigo, n + 1)

    def _desindexar_activo(self, p):
        """Desindexa un préstamo activo."""
        n = self.recursos_activos.buscar(p.recurso_codigo)
        if n is None:
            n = 0
        if n <= 1:
            self.recursos_activos.eliminar(p.recurso_codigo)
        else:
            self.recursos_activos.insertar(p.recurso_codigo, n - 1)

    def recurso_prestado(self, recurso_codigo):
        """
        ¿El recurso tiene al menos un préstamo activo (en cualquier sede)?

        Solo informativo: ya NO bloquea nuevos préstamos (eso lo decide el inventario).
        """
        return self.recursos_activos.buscar(recurso_codigo) is not None

    def registrar_prestamo(self, usuario_codigo, recurso_codigo, sede,
                           fecha_prestamo=None, dias_limite=14, _solicitud=None):
        """
        Registra un nuevo préstamo y descuenta 1 unidad de esa sede.

        Returns:
            str: código del préstamo (ej: "P0001"). Nunca devuelve None.

        Raises:
            ValueError: usuario inexistente o inactivo, recurso inexistente o
                        dado de baja, sede inexistente.
            SinUnidadesError (subclase de ValueError): la sede no tiene unidades.
        """
        # Validar usuario si gestor_usuarios está disponible
        if self.gestor_usuarios:
            usuario = self.gestor_usuarios.buscar_por_codigo(usuario_codigo)
            if usuario is None:
                raise ValueError(f"Usuario {usuario_codigo} no existe")
            # Un usuario dado de baja no puede recibir préstamos
            if not usuario.es_activo():
                raise ValueError(f"El usuario {usuario_codigo} esta inactivo")

        # Validar recurso si gestor_recursos está disponible
        if self.gestor_recursos:
            recurso = self.gestor_recursos.buscar_por_codigo(recurso_codigo)
            if recurso is None:
                raise ValueError(f"Recurso {recurso_codigo} no existe")
            if recurso.obtener_estado() == "Dado de baja":
                raise ValueError(f"El recurso {recurso_codigo} esta dado de baja")

            # Validar que la sede exista (buscando en la lista de sedes)
            sedes = self.gestor_recursos.listar_sedes()
            sede_existe = any(s.nombre == sede for s in sedes)
            if not sede_existe:
                raise ValueError(f"Sede '{sede}' no existe")

            # La disponibilidad se decide por el inventario de la sede (RQF-011),
            # no por si el recurso ya está prestado en otra parte. Se descuenta
            # al final de las validaciones para no restar una unidad y luego fallar.
            if not self.gestor_recursos.decrementar_disponibilidad(recurso_codigo, sede):
                raise SinUnidadesError(f"Sin unidades disponibles de {recurso_codigo} en {sede}")

        self.contador_codigos += 1
        codigo = f"P{self.contador_codigos:04d}"
        prestamo = Prestamo(codigo, usuario_codigo, recurso_codigo, sede,
                            fecha_prestamo, dias_limite)

        self.prestamos.agregar(prestamo)
        self.historial_simple.agregar_al_final(prestamo)
        self.historial_doble.agregar_al_final(prestamo)
        self.indice_codigo.insertar(codigo, prestamo)
        self._indexar_activo(prestamo)

        # Registrar el préstamo en el usuario (para contar préstamos activos)
        if self.gestor_usuarios:
            usuario = self.gestor_usuarios.buscar_por_codigo(usuario_codigo)
            if usuario:
                usuario.registrar_prestamo(codigo)

        self.pila_deshacer.push({
            'operacion': 'registrar_prestamo',
            'prestamo': prestamo,
            'solicitud': _solicitud,
        })
        return codigo

    def registrar_devolucion(self, codigo_prestamo):
        """
        Registra la devolución de un préstamo, suma 1 unidad a su sede y, si hay
        fila de espera para ese recurso, se lo asigna al siguiente (RQF-018).

        Returns (CAMBIO: antes solo True/False):
            False: el préstamo no existe o ya fue devuelto (no se hace nada).
            True:  devolución registrada; nadie esperaba el recurso.
            str:   devolución registrada y la unidad se asignó automáticamente;
                   es el código del préstamo nuevo (ej: "P0003").
            Los dos casos de éxito son verdaderos, así que `if resultado:` sigue
            sirviendo para saber si la devolución se hizo.

        Deshacer: si hubo asignación automática quedan DOS operaciones en la pila
        (la devolución y luego el préstamo automático). El primer deshacer revierte
        la asignación (el usuario vuelve al frente de la fila) y el segundo, la devolución.
        """
        p = self.indice_codigo.buscar(codigo_prestamo)
        if p is None or p.estado != "Activo":
            return False
        p.devolver()
        self._desindexar_activo(p)

        # La unidad vuelve a la sede donde se prestó (RQF-011)
        if self.gestor_recursos:
            self.gestor_recursos.incrementar_disponibilidad(p.recurso_codigo, p.sede)

        # Desregistrar el préstamo del usuario
        if self.gestor_usuarios:
            usuario = self.gestor_usuarios.buscar_por_codigo(p.usuario_codigo)
            if usuario:
                usuario.devolver_prestamo(codigo_prestamo)

        self.pila_deshacer.push({'operacion': 'registrar_devolucion', 'prestamo': p})

        # Atender la fila apenas queda una unidad libre (RF3 / RQF-018)
        if self.gestor_turnos and self.gestor_turnos.obtener_cantidad_espera(p.recurso_codigo) > 0:
            try:
                asignado = self.atender_siguiente_turno(p.recurso_codigo, p.sede)
            except ValueError:
                # La devolución ya quedó hecha; si la asignación falla, el usuario
                # vuelve al frente de la fila (lo hace atender_siguiente_turno).
                asignado = None
            if asignado:
                return asignado
        return True

    def deshacer(self):
        """
        Deshace la última operación registrada (Pila LIFO, RQF-015).

        - Deshacer préstamo: la unidad vuelve a la sede (+1). Si el préstamo salió
          de la fila de espera, el usuario vuelve al PRIMER lugar de la fila.
        - Deshacer devolución: la unidad se vuelve a descontar (-1).

        Raises:
            ValueError: si al deshacer una devolución ya no hay unidad para
                        descontar; la operación vuelve a la pila sin cambios.
        """
        op = self.pila_deshacer.pop()
        if op is None:
            return False

        p = op['prestamo']
        if op['operacion'] == 'registrar_prestamo':
            if p.estado == "Activo":
                self._desindexar_activo(p)
                # Solo si seguía activo: si ya estaba devuelto, la unidad ya volvió.
                if self.gestor_recursos:
                    self.gestor_recursos.incrementar_disponibilidad(p.recurso_codigo, p.sede)
            self.indice_codigo.eliminar(p.codigo)

            # Desregistrar del usuario
            if self.gestor_usuarios:
                usuario = self.gestor_usuarios.buscar_por_codigo(p.usuario_codigo)
                if usuario:
                    usuario.devolver_prestamo(p.codigo)

            # Quitar del vector
            restantes = [x for x in self.prestamos.recorrer() if x is not p]
            self.prestamos = VectorDinamico(capacidad_inicial=50)
            self.historial_simple = ListaSimple()
            self.historial_doble = ListaDoble()
            for x in restantes:
                self.prestamos.agregar(x)
                self.historial_simple.agregar_al_final(x)
                self.historial_doble.agregar_al_final(x)
            if _num(p.codigo) == self.contador_codigos:
                self.contador_codigos -= 1

            # E11: si el préstamo se asignó desde la fila, el usuario no pierde su
            # turno: vuelve al frente y la solicitud queda otra vez "En espera".
            solicitud = op.get('solicitud')
            if solicitud is not None and self.gestor_turnos:
                self.gestor_turnos.reinsertar_al_frente(solicitud)
        elif op['operacion'] == 'registrar_devolucion':
            # Se descuenta primero porque es lo único que puede fallar (si alguien
            # cambió el inventario a mano); así no queda el préstamo a medio revertir.
            if self.gestor_recursos and not self.gestor_recursos.decrementar_disponibilidad(p.recurso_codigo, p.sede):
                self.pila_deshacer.push(op)
                raise ValueError(f"No se puede deshacer la devolucion de {p.codigo}: "
                                 f"no quedan unidades de {p.recurso_codigo} en {p.sede}")
            p.reactivar()
            self._indexar_activo(p)

            # Re-registrar en el usuario
            if self.gestor_usuarios:
                usuario = self.gestor_usuarios.buscar_por_codigo(p.usuario_codigo)
                if usuario:
                    usuario.registrar_prestamo(p.codigo)
        return True

    def atender_siguiente_turno(self, recurso_codigo, sede):
        """
        Entrega una unidad del recurso en `sede` a quien sigue en la fila.

        Salta (y cancela) las solicitudes de usuarios que ya no están activos.
        Si el préstamo no se puede registrar, la solicitud vuelve al frente de
        la fila y se relanza el ValueError.

        Returns:
            str: código del préstamo creado, o None si la fila quedó vacía.
        """
        if self.gestor_turnos is None:
            raise ValueError("GestorPrestamos no tiene GestorTurnos asociado")
        while True:
            sol = self.gestor_turnos.obtener_siguiente(recurso_codigo)
            if sol is None:
                return None
            if self.gestor_usuarios:
                usuario = self.gestor_usuarios.buscar_por_codigo(sol.usuario_codigo)
                if usuario is None or not usuario.es_activo():
                    sol.cancelar()
                    continue
            try:
                return self.registrar_prestamo(sol.usuario_codigo, recurso_codigo, sede,
                                               _solicitud=sol)
            except ValueError:
                # obtener_siguiente() ya lo sacó de la fila; sin esto perdería el turno
                self.gestor_turnos.reinsertar_al_frente(sol)
                raise

    def listar_activos(self):
        """
        Préstamos con estado "Activo". O(n).

        Recorre el VectorDinamico por índice y devuelve otro VectorDinamico, para
        no construir una list de Python (regla del curso). Se usa con
        obtener_tamaño() y obtener(i).
        """
        activos = VectorDinamico(capacidad_inicial=10)
        for i in range(self.prestamos.obtener_tamaño()):
            p = self.prestamos.obtener(i)
            if p.estado == "Activo":
                activos.agregar(p)
        return activos

    def buscar_prestamo(self, codigo):
        """Busca por código — O(1) promedio con tabla hash."""
        return self.indice_codigo.buscar(codigo)

    def obtener_prestamos_usuario(self, usuario_codigo):
        """Préstamos activos de un usuario — O(n)."""
        return [p for p in self.prestamos.recorrer()
                if p.usuario_codigo == usuario_codigo and p.estado == "Activo"]

    def obtener_prestamos_atrasados(self, ahora=None):
        """Préstamos atrasados — O(n)."""
        return [p for p in self.prestamos.recorrer() if p.esta_atrasado(ahora)]

    def obtener_prestamos_sede(self, sede):
        """Préstamos activos de una sede específica."""
        return [p for p in self.prestamos.recorrer() if p.sede == sede and p.estado == "Activo"]

    def listar_todos(self):
        """Obtiene todos los préstamos."""
        return self.prestamos.recorrer()

    def obtener_cantidad(self):
        """Total de préstamos."""
        return self.prestamos.obtener_tamaño()

    def __str__(self):
        activos = len([p for p in self.prestamos.recorrer() if p.estado == "Activo"])
        return f"GestorPrestamos(total={self.obtener_cantidad()}, activos={activos})"
