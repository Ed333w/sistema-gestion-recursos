# CORRECCIONES DEL MENÚ — Repo proyecto beta (versión 4)

Trazabilidad de los cambios hechos para corregir los errores **E1 a E11** encontrados al
usar el menú. Este documento sirve para el informe de la Entrega 2 y para explicar cada
cambio sin abrir el código.

| Archivo de apoyo | Contenido |
|---|---|
| `CAMBIOS.diff` | Diff completo (`diff -u`) del original contra el corregido, solo de los archivos tocados |
| `evidencias/antes/` | Salida de cada comando de reproducción **antes** de corregir (sin modificar; solo se acortó la ruta del proyecto) |
| `evidencias/despues/` | Salida de los mismos comandos **después** de corregir |
| `evidencias/salida_test_*.txt` | Salida completa de las dos baterías de pruebas |
| `evidencias/scripts/` | Scripts usados para reproducir (`repro.sh`, `repro_e9_e11.py`, `repro_e6bc.py`) |

**Cómo verificar** (desde esta carpeta):

```bash
python -m pruebas.test_basico              # 8/8
python -m pruebas.test_correcciones_menu   # 13/13 (99 casos)
bash evidencias/scripts/repro.sh . salida  # los 7 comandos de reproducción → carpeta salida/
```

> **Nota Windows:** si la salida del programa se redirige (Git Bash, `| ...`, `> archivo`),
> Python 3.14 escribe en cp1252 y el carácter `═` del menú provoca `UnicodeEncodeError`.
> Ese problema **ya existía** y no forma parte de E1–E11. Para evitarlo, antes de ejecutar:
> `export PYTHONIOENCODING=utf-8` (Git Bash) o `$env:PYTHONIOENCODING="utf-8"` (PowerShell).
> En una consola normal sin redirección no ocurre.

---

## 5.1 Resumen en lenguaje sencillo

El programa tenía varios problemas al usarlo desde el menú. Algunas opciones lo cerraban de
golpe (listar préstamos activos, o registrar un usuario sin nombre). Otras decían que algo
había salido bien cuando no era así: devolvía "Devolucion registrada" para préstamos que no
existían, "Prestamo registrado: None" cuando no se prestaba nada, o "Categoria registrada"
aunque el código ya existía, y en ese caso borraba el nombre anterior. El inventario por sede
no cambiaba al prestar ni al devolver, solo se podía prestar un ejemplar de cada recurso aunque
hubiera cinco, se prestaba a usuarios dados de baja, no había forma de pedir turno en la fila de
espera, "ver siguiente" sacaba a la persona de la fila, los informes mostraban datos
equivocados y el inventario no aceptaba más de 100 recursos.

Ahora el programa nunca se cierra por un dato inválido: muestra un mensaje de error claro y
sigue funcionando. Se presta mientras haya unidades **en esa sede**: prestar resta una unidad,
devolver la suma y deshacer revierte el conteo. Si no quedan unidades, el programa ofrece
entrar a la fila de espera, y cuando alguien devuelve el recurso se le asigna automáticamente
al primero de la fila. Si ese préstamo automático se deshace, la persona vuelve al primer lugar
y no pierde su turno. "Ver siguiente" solo consulta, las categorías no se repiten, los informes
muestran préstamos y recursos reales, y el inventario crece solo, así que acepta 500 recursos o
más.

---

## 5.2 Fichas por error

Los números de línea son los del archivo **nuevo** (aproximados). En las salidas se omiten con
`[...]` las repeticiones del menú; el texto completo está en `evidencias/`.

### E1 — "Listar préstamos activos" cerraba el programa

**Antes (comportamiento):** Préstamos → 3 terminaba el programa con
`AttributeError: 'GestorPrestamos' object has no attribute 'listar_activos'`.
**Causa:** `main.py` llamaba a `gestor_prestamos.listar_activos()`, pero ese método nunca se
escribió en `GestorPrestamos`.
**Ahora (comportamiento):** muestra el total y los préstamos con estado "Activo"; si no hay
ninguno, muestra "Total prestamos activos: 0".

**Archivos y funciones modificados:**
- `modulos/M03_prestamos/gestor_prestamos.py` → método **nuevo** `listar_activos` (líneas 280–293)
- `main.py` → `gestion_prestamos`, opción 3 (líneas 431–437)

**Código ANTES** — `gestor_prestamos.py`: el método no existía. `main.py`:
```python
        elif opcion == "3":
            prestamos = gestor_prestamos.listar_activos()
            print(f"\nTotal prestamos activos: {len(prestamos)}\n")
            for p in prestamos:
                print(f"  {p.codigo}: {p.usuario_codigo} -> {p.recurso_codigo} [{p.sede}]")
```

**Código DESPUÉS** — `gestor_prestamos.py`:
```python
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
```
`main.py`:
```python
        elif opcion == "3":
            # listar_activos devuelve un VectorDinamico (no una list)
            activos = gestor_prestamos.listar_activos()
            print(f"\nTotal prestamos activos: {activos.obtener_tamaño()}\n")
            for i in range(activos.obtener_tamaño()):
                p = activos.obtener(i)
                print(f"  {p.codigo}: {p.usuario_codigo} -> {p.recurso_codigo} [{p.sede}]")
```

**Por qué se hizo así:** el curso prohíbe usar `list` como colección del sistema. Como
`VectorDinamico.recorrer()` arma una `list`, aquí se recorre por índice con `obtener(i)` y el
resultado se guarda en otro `VectorDinamico`. Por eso el menú usa `obtener_tamaño()` en lugar
de `len()`. Complejidad O(n), con n = préstamos registrados.
**Estructura de datos involucrada:** `VectorDinamico` (`self.prestamos` y el resultado).
**Requisito que satisface:** consulta de préstamos activos de M03 (menú Préstamos → 3).
**Salida del comando de reproducción — ANTES** (`evidencias/antes/E1.txt`):
```
 Prestamo registrado: P0001
[...]
Selecciona opcion: Traceback (most recent call last):
  File "<proyecto_original>\main.py", line 702, in <module>
    main()
    ~~~~^^
  File "<proyecto_original>\main.py", line 678, in main
    gestion_prestamos(gestor_prestamos, gestor_usuarios, gestor_recursos)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<proyecto_original>\main.py", line 393, in gestion_prestamos
    prestamos = gestor_prestamos.listar_activos()
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'GestorPrestamos' object has no attribute 'listar_activos'. Did you mean: 'listar_todos'?
exit=1
```
**Salida del comando de reproducción — DESPUÉS** (`evidencias/despues/E1.txt`):
```
 Prestamo registrado: P0001
[...]
Total prestamos activos: 1

  P0001: U001 -> R0001 [Centro]
[...]
¡Hasta luego! 
exit=0
```
**Prueba que lo verifica:** `test_e1_listar_activos` (incluye lista vacía, solo activos y menú).

---

### E2 — Errores de datos que cerraban el programa (`ValueError` sin capturar)

**Antes (comportamiento):** Usuarios → 1 con nombre vacío terminaba el programa con un
`Traceback` de `ValueError`.
**Causa:** `GestorUsuarios.registrar` validaba bien y lanzaba `ValueError`, pero `main.py` no
lo capturaba. Además, en Préstamos se usaba `except Exception`, que oculta errores de
programación (el `AttributeError` de E1, por ejemplo, se habría mostrado como "Error: …").
**Ahora (comportamiento):** muestra `Error: El nombre del usuario no puede estar vacío` y el
programa continúa. Todas las llamadas del menú que pueden lanzar `ValueError` lo capturan.

**Archivos y funciones modificados:** solo `main.py`:

| Menú | Llamada | Cambio | Líneas |
|---|---|---|---|
| Usuarios → 1 | `registrar` | `try/except ValueError` nuevo | 252–261 |
| Préstamos → 1 | `registrar_prestamo` | `except Exception` → `except SinUnidadesError` + `except ValueError` | 391–411 |
| Préstamos → 2 | `registrar_devolucion` | `except Exception` → `except ValueError` | 413–429 |
| Préstamos → 8 | `deshacer` | `try/except ValueError` nuevo (ahora puede lanzar, ver E4) | 473–481 |
| Turnos → 4 (nueva) | `solicitar_turno` | `try/except ValueError` en `solicitar_turno_menu` | 354–362 |
| Categorías → 1 | `registrar_categoria` | `try/except ValueError` nuevo (ver E7) | 568–574 |
| Recursos → 1, 2, 3 | `registrar_libro/equipo/sala` | **Revisado, sin cambios**: libro y sala ya tenían `try/except ValueError` para el año y la capacidad; los constructores y `registrar_equipo` no lanzan `ValueError` | — |

**Código ANTES** — `main.py`, Usuarios → 1:
```python
            nombre = input("\nNombre: ")
            email = input("Email: ")
            codigo = gestor.registrar(nombre, email)
            print(f"\n Usuario registrado: {codigo}")
```
**Código DESPUÉS:**
```python
            nombre = input("\nNombre: ")
            email = input("Email: ")
            # registrar() lanza ValueError si nombre o email están vacíos;
            # sin el try el programa se cerraba con un Traceback.
            try:
                codigo = gestor.registrar(nombre, email)
                print(f"\n Usuario registrado: {codigo}")
            except ValueError as e:
                print(f"\n Error: {e}")
```
(Los pares antes/después de Préstamos 1, 2 y 8 están en las fichas E3, E5 y E4; el de Categorías, en E7.)

**Por qué se hizo así:** sigue la convención del proyecto: los gestores lanzan `ValueError`
con un mensaje claro y `main.py` lo muestra. Se capturó `ValueError` y no `Exception` para
que un error de datos se muestre como mensaje, pero un error de programación siga siendo visible.
**Estructura de datos involucrada:** ninguna (manejo de excepciones en el menú).
**Requisito que satisface:** RNF de robustez: el programa no se cierra por un dato inválido.
**Salida del comando de reproducción — ANTES** (`evidencias/antes/E2.txt`):
```
Nombre: Email: Traceback (most recent call last):
  File "<proyecto_original>\main.py", line 702, in <module>
    main()
    ~~~~^^
  File "<proyecto_original>\main.py", line 669, in main
    gestion_usuarios(gestor_usuarios)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "<proyecto_original>\main.py", line 254, in gestion_usuarios
    codigo = gestor.registrar(nombre, email)
  File "<proyecto_original>\modulos\M01_usuarios\gestor_usuarios.py", line 118, in registrar
    raise ValueError("El nombre del usuario no puede estar vacío")
ValueError: El nombre del usuario no puede estar vacío
exit=1
```
**Salida del comando de reproducción — DESPUÉS** (`evidencias/despues/E2.txt`):
```
Nombre: Email: 
 Error: El nombre del usuario no puede estar vacío

Presione Enter para continuar...
[...]
¡Hasta luego! 
exit=0
```
**Prueba que lo verifica:** `test_e2_errores_capturados` (nombre vacío, email en blanco,
usuario válido, usuario U999, sede inexistente y deshacer sin operaciones, todo desde el menú).

---

### E3 — Segundo préstamo de un recurso con ejemplares disponibles

**Antes (comportamiento):** el segundo préstamo de R0001 en Centro mostraba
"Prestamo registrado: None", aunque había 5 ejemplares.
**Causa:** el modo `exclusivo` (`recurso_prestado`) permitía un solo préstamo activo por recurso
en todo el sistema y no consultaba el inventario. Al bloquear, devolvía `None` y el menú lo imprimía.
**Ahora (comportamiento):** se puede prestar mientras haya unidades en esa sede. Sin unidades,
aparece `Error: Sin unidades disponibles de R0001 en Centro` y el menú pregunta si se quiere
pedir turno. Nunca se imprime "Prestamo registrado: None".

**Archivos y funciones modificados:**
- `modulos/M03_prestamos/gestor_prestamos.py` → clase **nueva** `SinUnidadesError` (líneas 11–17);
  `__init__` (se quitó `exclusivo`, líneas 23–45); `recurso_prestado` (solo docstring, 64–70);
  `registrar_prestamo` (líneas 72–136); `atender_siguiente_turno` (se quitó la regla, ver E6c)
- `modulos/M03_prestamos/__init__.py` → exporta `SinUnidadesError`
- `main.py` → import (línea 14); `gestion_prestamos`, opción 1 (líneas 391–411)

**Código ANTES** — `gestor_prestamos.py`:
```python
    def __init__(self, gestor_turnos=None, exclusivo=True, gestor_usuarios=None, gestor_recursos=None):
        """
        gestor_turnos: GestorTurnos (M04) opcional, para integrar turnos.
        exclusivo: si True, un recurso no puede tener dos préstamos activos a la vez.
        ...
        self.exclusivo = exclusivo
    ...
    def recurso_prestado(self, recurso_codigo):
        """¿Un recurso está prestado (en modo exclusivo)?"""
        return self.recursos_activos.buscar(recurso_codigo) is not None
    ...
        # (en registrar_prestamo y en atender_siguiente_turno)
        if self.exclusivo and self.recurso_prestado(recurso_codigo):
            return None
```
**Código DESPUÉS** — `gestor_prestamos.py`:
```python
class SinUnidadesError(ValueError):
    """
    No quedan unidades del recurso en la sede pedida.

    Es un ValueError (se captura igual que los demás errores de datos), pero con
    nombre propio para que el menú distinga este caso y ofrezca pedir turno.
    """
...
    def __init__(self, gestor_turnos=None, gestor_usuarios=None, gestor_recursos=None):
...
    def recurso_prestado(self, recurso_codigo):
        """
        ¿El recurso tiene al menos un préstamo activo (en cualquier sede)?

        Solo informativo: ya NO bloquea nuevos préstamos (eso lo decide el inventario).
        """
...
            # La disponibilidad se decide por el inventario de la sede (RQF-011),
            # no por si el recurso ya está prestado en otra parte. Se descuenta
            # al final de las validaciones para no restar una unidad y luego fallar.
            if not self.gestor_recursos.decrementar_disponibilidad(recurso_codigo, sede):
                raise SinUnidadesError(f"Sin unidades disponibles de {recurso_codigo} en {sede}")
```
**Código ANTES** — `main.py`, Préstamos → 1:
```python
            try:
                codigo_prestamo = gestor_prestamos.registrar_prestamo(usuario_cod, recurso_cod, sede)
                print(f"\n Prestamo registrado: {codigo_prestamo}")
            except Exception as e:
                print(f"\n Error: {e}")
```
**Código DESPUÉS:**
```python
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
```

**Por qué se hizo así:** el inventario es por sede (RQF-009/011), así que la pregunta correcta
es "¿quedan unidades en esta sede?" y no "¿está prestado en algún lado?". `decrementar_disponibilidad`
ya existía y devuelve `False` si no hay unidades, de modo que la misma llamada valida y descuenta.
`SinUnidadesError` hereda de `ValueError`: cualquier `except ValueError` lo sigue capturando, y el
menú puede reconocer este caso sin comparar el texto del mensaje. `recurso_prestado` se dejó
(ahora solo informa) porque quitarlo obligaba a borrar también el índice `recursos_activos` y
sus dos métodos auxiliares, un cambio mayor sin beneficio para estas correcciones.
**Estructura de datos involucrada:** la matriz `[sede][recurso]` de `GestorInventario` (a través de `GestorRecursos`).
**Requisito que satisface:** RQF-009, RQF-011 y RF3 (ofrecer turno cuando no hay unidades).
**Salida del comando de reproducción — ANTES** (`evidencias/antes/E3E4.txt`):
```
Codigo usuario: Codigo recurso: Sede (Centro/Norte/Sur): 
 Prestamo registrado: P0001
[...]
Codigo usuario: Codigo recurso: Sede (Centro/Norte/Sur): 
 Prestamo registrado: None
```
**Salida del comando de reproducción — DESPUÉS** (`evidencias/despues/E3E4.txt` y `E6_extra_turno.txt`):
```
Codigo usuario: Codigo recurso: Sede (Centro/Norte/Sur): 
 Prestamo registrado: P0001
[...]
Codigo usuario: Codigo recurso: Sede (Centro/Norte/Sur): 
 Prestamo registrado: P0002
```
```
# R0003 tiene 1 unidad: U001 la presta y U002 lo intenta y responde "s"
 Error: Sin unidades disponibles de R0003 en Centro
¿Desea pedir turno en la fila de espera? (s/n): 
 Turno S0001 asignado, posicion 1 en la fila
```
**Prueba que lo verifica:** `test_e3_disponibilidad_por_sede`.

---

### E4 — Prestar no descontaba inventario y devolver no lo sumaba

**Antes (comportamiento):** después de prestar R0001 dos veces, la matriz de Inventario seguía
mostrando 5 en Centro.
**Causa:** `GestorPrestamos` nunca llamaba a `decrementar_disponibilidad` ni a
`incrementar_disponibilidad` de `GestorRecursos`, aunque ya existían.
**Ahora (comportamiento):** prestar → −1 en la sede; devolver → +1 en la sede del préstamo;
deshacer préstamo → +1; deshacer devolución → −1. La matriz del menú lo refleja.

**Archivos y funciones modificados:** `modulos/M03_prestamos/gestor_prestamos.py` →
`registrar_prestamo` (descuento, líneas 108–112, ver E3), `registrar_devolucion` (+1, líneas 161–163),
`deshacer` (líneas 185–248).

**Código ANTES** — `registrar_devolucion` y `deshacer`:
```python
        p.devolver()
        self._desindexar_activo(p)

        # Desregistrar el préstamo del usuario
...
        if op['operacion'] == 'registrar_prestamo':
            if p.estado == "Activo":
                self._desindexar_activo(p)
            self.indice_codigo.eliminar(p.codigo)
...
        elif op['operacion'] == 'registrar_devolucion':
            p.reactivar()
            self._indexar_activo(p)
```
**Código DESPUÉS:**
```python
        p.devolver()
        self._desindexar_activo(p)

        # La unidad vuelve a la sede donde se prestó (RQF-011)
        if self.gestor_recursos:
            self.gestor_recursos.incrementar_disponibilidad(p.recurso_codigo, p.sede)
...
        if op['operacion'] == 'registrar_prestamo':
            if p.estado == "Activo":
                self._desindexar_activo(p)
                # Solo si seguía activo: si ya estaba devuelto, la unidad ya volvió.
                if self.gestor_recursos:
                    self.gestor_recursos.incrementar_disponibilidad(p.recurso_codigo, p.sede)
            self.indice_codigo.eliminar(p.codigo)
...
        elif op['operacion'] == 'registrar_devolucion':
            # Se descuenta primero porque es lo único que puede fallar (si alguien
            # cambió el inventario a mano); así no queda el préstamo a medio revertir.
            if self.gestor_recursos and not self.gestor_recursos.decrementar_disponibilidad(p.recurso_codigo, p.sede):
                self.pila_deshacer.push(op)
                raise ValueError(f"No se puede deshacer la devolucion de {p.codigo}: "
                                 f"no quedan unidades de {p.recurso_codigo} en {p.sede}")
            p.reactivar()
            self._indexar_activo(p)
```

**Por qué se hizo así:** se usa la sede guardada en el préstamo (`p.sede`), así la unidad
vuelve al lugar de donde salió. Al deshacer una devolución, la unidad puede ya no estar si
alguien cambió el inventario a mano con `actualizar_disponibilidad`, que no pasa por la pila.
En ese caso la operación se devuelve a la pila y se lanza `ValueError`: el historial queda
intacto y el menú muestra el motivo. Todas las operaciones son O(1).
**Estructura de datos involucrada:** matriz de inventario (`GestorInventario`) y la `Pila` de deshacer.
**Requisito que satisface:** RQF-009, RQF-011, RQF-015.
**Salida del comando de reproducción — ANTES** (`evidencias/antes/E3E4.txt`):
```
Sede\Recurso    | R0001 | R0002 | R0003
---------------------------------------
Centro          | 5     | 2     | 1    
```
**Salida del comando de reproducción — DESPUÉS** (`evidencias/despues/E3E4.txt`):
```
Sede\Recurso    | R0001 | R0002 | R0003
---------------------------------------
Centro          | 3     | 2     | 1    
```
**Prueba que lo verifica:** `test_e4_inventario` (5 préstamos → 0, devolver → 1, deshacer
devolución → 0, deshacer préstamo → 1, y el caso límite del inventario cambiado a mano).

---

### E5 — Devolver un préstamo inexistente decía "Devolucion registrada"

**Antes (comportamiento):** devolver P9999 mostraba "Devolucion registrada".
**Causa:** `registrar_devolucion` indica el fallo devolviendo `False` (no lanza error), y el
menú no revisaba lo que devolvía.
**Ahora (comportamiento):** `Error: El prestamo P9999 no existe o ya fue devuelto`.

**Archivos y funciones modificados:** `main.py` → `gestion_prestamos`, opción 2 (líneas 413–429).

**Código ANTES:**
```python
            codigo_prestamo = input("\nCodigo prestamo: ")
            try:
                gestor_prestamos.registrar_devolucion(codigo_prestamo)
                print(f"\n Devolucion registrada")
            except Exception as e:
                print(f"\n Error: {e}")
```
**Código DESPUÉS:**
```python
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
```

**Por qué se hizo así:** se respeta el retorno `False` que ya usaba el gestor (convención
del proyecto) y el menú lo revisa. El mismo bloque muestra la asignación automática de E6c.
**Estructura de datos involucrada:** `TablaHash` `indice_codigo` (la búsqueda del préstamo, O(1) promedio).
**Requisito que satisface:** registro de devoluciones de M03; RNF de mensajes claros.
**Salida del comando de reproducción — ANTES** (`evidencias/antes/E5.txt`):
```
Codigo prestamo: 
 Devolucion registrada
```
**Salida del comando de reproducción — DESPUÉS** (`evidencias/despues/E5.txt`):
```
Codigo prestamo: 
 Error: El prestamo P9999 no existe o ya fue devuelto
```
**Prueba que lo verifica:** `test_e5_devolucion_inexistente` (P9999, devolver dos veces el mismo, menú).

---

### E6a — No había opción para pedir turno

**Antes (comportamiento):** el menú Turnos solo tenía "Ver siguiente", "Ver fila" y "Ver cantidad";
la cola nunca se llenaba desde el programa.
**Causa:** no existía la opción y `GestorTurnos` solo tenía `encolar`, sin validaciones y sin
acceso a usuarios ni recursos.
**Ahora (comportamiento):** Turnos → **4. Solicitar turno** (usuario, recurso, sede) valida
los datos y muestra "Turno S0001 asignado, posicion 2 en la fila". También se llega desde
Préstamos → 1 cuando no hay unidades (E3).

**Archivos y funciones modificados:**
- `modulos/M04_turnos/gestor_turnos.py` → `__init__` (recibe gestores, líneas 9–21); métodos
  **nuevos** `esta_en_espera` (42–50) y `solicitar_turno` (52–95)
- `main.py` → función **nueva** `solicitar_turno_menu` (354–362); `gestion_turnos`: opción **nueva** 4
  (líneas 507 y 536–541); `main()`: construcción de `GestorTurnos` (682–686); texto del menú principal (línea 55)

**Código ANTES** — `gestor_turnos.py`:
```python
    def __init__(self):
        self.colas = TablaHash(211)  # {recurso_codigo: ColaFIFO de Solicitudes}
        self.solicitudes = TablaHash(211)  # {codigo_solicitud: Solicitud}
        self.contador = 0
```
`main.py`:
```python
        print("\n1. Ver siguiente turno")
        print("2. Ver fila de espera (por recurso)")
        print("3. Ver cantidad en espera")
        print("0. Volver")
...
    gestor_turnos = GestorTurnos()
```
**Código DESPUÉS** — `gestor_turnos.py`:
```python
    def __init__(self, gestor_usuarios=None, gestor_recursos=None):
        ...
        self.gestor_usuarios = gestor_usuarios
        self.gestor_recursos = gestor_recursos

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
        ...
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
```
`main.py`:
```python
def solicitar_turno_menu(gestor_turnos, usuario_cod, recurso_cod, sede):
    """Pide turno y muestra la posición. Lo usan los menús de Turnos y de Préstamos."""
    try:
        codigo = gestor_turnos.solicitar_turno(usuario_cod, recurso_cod, sede)
        # La solicitud entra al final, así que su posición es el tamaño de la fila
        posicion = gestor_turnos.obtener_cantidad_espera(recurso_cod)
        print(f"\n Turno {codigo} asignado, posicion {posicion} en la fila")
    except ValueError as e:
        print(f"\n Error: {e}")
...
        print("4. Solicitar turno")
...
        elif opcion == "4":
            # Antes no había forma de entrar a la fila desde el programa (RF3)
            usuario_cod = input("\nCodigo usuario: ")
            recurso_cod = input("Codigo recurso: ")
            sede = input("Sede (Centro/Norte/Sur): ")
            solicitar_turno_menu(gestor_turnos, usuario_cod, recurso_cod, sede)
...
    # GestorTurnos recibe usuarios y recursos para validar "Solicitar turno"
    gestor_turnos = GestorTurnos(
        gestor_usuarios=gestor_usuarios,
        gestor_recursos=gestor_recursos
    )
```

**Por qué se hizo así:** los gestores se pasan a `GestorTurnos` igual que a `GestorPrestamos`
(parámetros opcionales), así que `GestorTurnos()` sigue funcionando. Las validaciones están en el
gestor y no en el menú, para que se puedan probar. La opción se agregó como **4** para no cambiar
el número de las existentes (los comandos de reproducción siguen sirviendo). La búsqueda de
duplicados recorre solo la fila de ese recurso (O(n), n pequeño); un índice extra en `TablaHash`
habría que mantenerlo sincronizado en cuatro métodos. `encolar` se dejó sin validaciones porque
es la operación básica de la cola.
**Estructura de datos involucrada:** `ColaFIFO` por recurso (dentro de una `TablaHash`).
**Requisito que satisface:** RF3, RQF-016, RQF-017.
**Salida del comando de reproducción — ANTES** (`evidencias/antes/E6.txt`):
```
1. Ver siguiente turno
2. Ver fila de espera (por recurso)
3. Ver cantidad en espera
0. Volver

Selecciona opcion: 
Codigo recurso: 
  No hay nadie en fila para R0001
[...]
Fila para R0001: 0 personas
```
**Salida del comando de reproducción — DESPUÉS** (`evidencias/despues/E6.txt`: mismo comando, ahora aparece la
opción 4; `evidencias/despues/E6_extra_turno.txt`: pedir turno de verdad):
```
1. Ver siguiente turno
2. Ver fila de espera (por recurso)
3. Ver cantidad en espera
4. Solicitar turno
0. Volver
```
```
 Error: Sin unidades disponibles de R0003 en Centro
¿Desea pedir turno en la fila de espera? (s/n): 
 Turno S0001 asignado, posicion 1 en la fila
```
**Prueba que lo verifica:** `test_e6a_solicitar_turno` (con unidades → rechazado, duplicado →
rechazado, usuario/recurso/sede inexistentes, usuario inactivo, posiciones 1 y 2, menú).

---

### E6b — "Ver siguiente turno" sacaba al usuario de la fila

**Antes (comportamiento):** consultar quién seguía desencolaba la solicitud y la marcaba "Otorgado";
el usuario perdía su turno sin recibir nada.
**Causa:** el menú usaba `obtener_siguiente`, que desencola.
**Ahora (comportamiento):** solo consulta; la fila no cambia.

**Archivos y funciones modificados:** `gestor_turnos.py` → método **nuevo** `ver_siguiente`
(97–108) y docstring de `obtener_siguiente` (110–115); `main.py` → `gestion_turnos`, opción 1 (518–523).

**Código ANTES** — `main.py`:
```python
            siguiente = gestor_turnos.obtener_siguiente(recurso)
            if siguiente:
                print(f"\n Siguiente en fila: {siguiente.usuario_codigo}")
```
**Código DESPUÉS** — `gestor_turnos.py`:
```python
    def ver_siguiente(self, recurso_codigo):
        """
        Consulta quién sigue en la fila SIN sacarlo. O(1).
        ...
        """
        cola = self.colas.buscar(recurso_codigo)
        if cola is None:
            return None
        return cola.frente()
```
`main.py`:
```python
            # ver_siguiente solo consulta; obtener_siguiente sacaba al usuario de la fila
            siguiente = gestor_turnos.ver_siguiente(recurso)
            if siguiente:
                print(f"\n Siguiente en fila: {siguiente.usuario_codigo} (turno {siguiente.codigo})")
```

**Por qué se hizo así:** `ColaFIFO.frente()` ya existía y devuelve el primero sin quitarlo (O(1)).
`obtener_siguiente` se mantiene porque es la operación correcta **al asignar** el recurso.
**Estructura de datos involucrada:** `ColaFIFO` (`frente` en vez de `desencolar`).
**Requisito que satisface:** RF3 / RQF-016 (orden estricto de llegada: consultar no altera la fila).
**Salida — ANTES** (el menú no podía llenar la fila, así que se usó `evidencias/scripts/repro_e6bc.py` con
la misma llamada que hacía el menú; `evidencias/antes/E6b_E6c.txt`):
```
E6b: 'Ver siguiente' muestra U002 | personas en fila después de mirar: 0 | estado S0001: Otorgado
```
**Salida — DESPUÉS** (`evidencias/despues/E6b_E6c.txt` y, desde el menú, `E6_extra_turno.txt`):
```
E6b: 'Ver siguiente' muestra U002 | personas en fila después de mirar: 1 | estado S0001: En espera
```
```
 Siguiente en fila: U002 (turno S0001)
[...]
 Siguiente en fila: U002 (turno S0001)
[...]
Fila para R0003: 1 personas
```
**Prueba que lo verifica:** `test_e6b_ver_siguiente` (cola vacía, un elemento, el tamaño no cambia, menú).

---

### E6c — La fila no se atendía al devolver

**Antes (comportamiento):** al devolver un recurso con gente esperando, la unidad quedaba libre y la
fila seguía igual.
**Causa:** `registrar_devolucion` no consultaba la fila; `atender_siguiente_turno` existía pero nadie
lo llamaba, y además tenía la regla `exclusivo`.
**Ahora (comportamiento):** si la fila del recurso no está vacía, la unidad devuelta se presta
automáticamente al siguiente (en la sede del préstamo devuelto). Se saltan los usuarios que ya no están
activos. El menú muestra "Asignado automaticamente a U002 (siguiente en la fila): P0003".

**Archivos y funciones modificados:** `gestor_prestamos.py` → `registrar_devolucion` (138–183, **cambia
el retorno**), `atender_siguiente_turno` (250–278); `main.py` → Préstamos → 2 (ver E5).

**Código ANTES** — `gestor_prestamos.py`:
```python
        self.pila_deshacer.push({'operacion': 'registrar_devolucion', 'prestamo': p})
        return True
...
    def atender_siguiente_turno(self, recurso_codigo, sede):
        """Entrega el recurso a quien sigue en la cola."""
        if self.gestor_turnos is None:
            raise ValueError("GestorPrestamos no tiene GestorTurnos asociado")
        if self.exclusivo and self.recurso_prestado(recurso_codigo):
            return None
        sol = self.gestor_turnos.obtener_siguiente(recurso_codigo)
        if sol is None:
            return None
        return self.registrar_prestamo(sol.usuario_codigo, recurso_codigo, sede,
                                       _solicitud=sol)
```
**Código DESPUÉS:**
```python
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
...
    def atender_siguiente_turno(self, recurso_codigo, sede):
        ...
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
```

**Cambio de retorno de `registrar_devolucion`** (documentado en su docstring):

| Retorno | Significado |
|---|---|
| `False` | el préstamo no existe o ya fue devuelto (igual que antes) |
| `True` | devolución registrada; nadie esperaba el recurso (igual que antes) |
| `str` (ej. `"P0003"`) | **nuevo:** devolución registrada y la unidad se asignó al siguiente de la fila; es el código del préstamo automático |

Los dos casos de éxito son verdaderos, así que el código que hacía `if gp.registrar_devolucion(x):`
sigue funcionando. Quien llama: `main.py` (actualizado). Ningún otro archivo la usa.

**Por qué se hizo así:** la asignación pasa por `registrar_prestamo`, así que reutiliza todas sus
validaciones, el descuento de inventario y el registro en la pila. Las solicitudes de usuarios
inactivos se marcan "Cancelado" y se pasa al siguiente. Si el préstamo automático falla (por ejemplo,
porque el recurso fue dado de baja), la solicitud vuelve al frente y la devolución igual queda registrada.
**Estructura de datos involucrada:** `ColaFIFO` (desencolar), matriz de inventario y `Pila`.
**Requisito que satisface:** RF3, RQF-018 ("se asigna al siguiente apenas quede una disponible").
**Salida — ANTES** (`evidencias/antes/E6b_E6c.txt`):
```
E6c: registrar_devolucion devuelve True | fila después: ['U002'] | préstamos activos de U002: 0
```
**Salida — DESPUÉS** (`evidencias/despues/E6b_E6c.txt` y, desde el menú, `E6c_E11_extra.txt`):
```
E6c: registrar_devolucion devuelve 'P0002' | fila después: [] | préstamos activos de U002: 1
```
```
Codigo prestamo: 
 Devolucion registrada
 Asignado automaticamente a U002 (siguiente en la fila): P0002
[...]
Total prestamos activos: 1

  P0002: U002 -> R0003 [Centro]
```
**Prueba que lo verifica:** `test_e6c_atender_al_devolver` (sin fila → `True`; fila [U002, U003] →
préstamo para U002 y fila [U003]; usuario inactivo saltado; fila solo con inactivos; menú).

---

### E7 — Categoría repetida sobrescribía el nombre

**Antes (comportamiento):** registrar C1 dos veces mostraba "registrada" las dos veces y la segunda
sobrescribía el nombre.
**Causa:** `GestorCategorias` guardaba las categorías en un `dict` de Python (prohibido por el curso)
y asignaba `self.categorias[codigo] = cat` sin revisar si ya existía.
**Ahora (comportamiento):** `Error: La categoria C1 ya existe`; C1 conserva su nombre original.

**Archivos y funciones modificados:** `modulos/M05_categorias/gestor_categorias.py` → import (línea 3),
`__init__` (34–39), `registrar_categoria` (41–65), `obtener_categoria` (67–79), `obtener_cantidad` (81–83);
`main.py` → Categorías → 1 (568–574).

**Código ANTES:**
```python
from estructuras import ArbolBinario
...
        self.arbol = ArbolBinario()
        self.categorias = {}
...
        cat = Categoria(codigo, nombre)
        self.categorias[codigo] = cat
...
        return self.categorias.get(codigo)
...
        return len(self.categorias)
```
`main.py`:
```python
            gestor_categorias.registrar_categoria(codigo, nombre)
            print(f"\n Categoria registrada: {codigo}")
```
**Código DESPUÉS:**
```python
from estructuras import ArbolBinario, TablaHash
...
        self.arbol = ArbolBinario()
        # Antes era un dict de Python; el curso exige estructuras propias y
        # la TablaHash permite comprobar en O(1) promedio si un código ya existe.
        self.categorias = TablaHash(211)  # código -> Categoria
...
        # Sin esta validación, insertar() de la TablaHash actualiza el valor y la
        # segunda categoría C1 sobrescribía el nombre de la primera.
        if self.categorias.contiene(codigo):
            raise ValueError(f"La categoria {codigo} ya existe")
        cat = Categoria(codigo, nombre)
        self.categorias.insertar(codigo, cat)
...
        return self.categorias.buscar(codigo)
...
        return self.categorias.obtener_cantidad()
```
`main.py`:
```python
            # registrar_categoria lanza ValueError si el código ya existe (RF7)
            try:
                gestor_categorias.registrar_categoria(codigo, nombre)
                print(f"\n Categoria registrada: {codigo}")
            except ValueError as e:
                print(f"\n Error: {e}")
```

**Por qué se hizo así:** el prompt pide comprobarlo con la `TablaHash` del proyecto, y eso además
elimina el `dict`. Se valida **antes** de insertar en el árbol, así que el árbol tampoco recibe
duplicados. `contiene`, `buscar` e `insertar` son O(1) promedio.
**Estructura de datos involucrada:** `TablaHash` (unicidad de códigos) + `ArbolBinario` (sin cambios).
**Requisito que satisface:** RF7 (categorías sin repetidos).
**Salida del comando de reproducción — ANTES** (`evidencias/antes/E7.txt`):
```
 Categoria registrada: C1
[...]
 Categoria registrada: C1
[...]
  C1: Repetida
```
**Salida del comando de reproducción — DESPUÉS** (`evidencias/despues/E7.txt`):
```
 Categoria registrada: C1
[...]
 Error: La categoria C1 ya existe
[...]
  C1: Ingenieria
```
**Prueba que lo verifica:** `test_e7_categoria_repetida`.

---

### E8 — Los informes mostraban datos equivocados

**Antes (comportamiento):** "Reporte de uso" decía "Total de préstamos registrados: 3" (eran los 3
recursos) y "Reporte de inventario" imprimía los usuarios.
**Causa:** el constructor es `GeneradorInformes(gestor_recursos, gestor_prestamos)`, pero `main()` lo
llamaba por posición con `(gestor_usuarios, gestor_recursos)`: los usuarios quedaban como "recursos" y
los recursos como "préstamos".
**Ahora (comportamiento):** el reporte de uso cuenta los préstamos reales y el de inventario muestra los recursos.

**Archivos y funciones modificados:** `main.py` → `main()` (líneas 693–698).

**Código ANTES:**
```python
    generador_informes = GeneradorInformes(gestor_usuarios, gestor_recursos)
```
**Código DESPUÉS:**
```python
    # Argumentos con nombre: antes se pasaba (gestor_usuarios, gestor_recursos) por
    # posición y el reporte de uso contaba recursos y el de inventario mostraba usuarios.
    generador_informes = GeneradorInformes(
        gestor_recursos=gestor_recursos,
        gestor_prestamos=gestor_prestamos
    )
```

**Por qué se hizo así:** con argumentos con nombre, el orden ya no importa y Python da error si el
nombre está mal escrito, así que no vuelve a pasar. `GeneradorInformes` no se tocó.
**Estructura de datos involucrada:** ninguna (conexión entre módulos).
**Requisito que satisface:** informes de M06 (uso e inventario).
**Salida del comando de reproducción — ANTES** (`evidencias/antes/E8.txt`):
```
 REPORTE DE USO:
Total de préstamos registrados: 3
[...]
 REPORTE DE INVENTARIO:
GestorUsuarios(total=2, activos=2)
```
**Salida del comando de reproducción — DESPUÉS** (`evidencias/despues/E8.txt`):
```
 REPORTE DE USO:
Total de préstamos registrados: 1
[...]
 REPORTE DE INVENTARIO:
GestorRecursos(libros=1, equipos=1, salas=1)
```
**Prueba que lo verifica:** `test_e8_informes`.

---

### E9 — Se prestaba a usuarios inactivos y recursos dados de baja

**Antes (comportamiento):** un préstamo a un usuario INACTIVO se aceptaba (`P0001`); lo mismo con un
recurso "Dado de baja".
**Causa:** `registrar_prestamo` solo verificaba que el usuario y el recurso **existieran**.
**Ahora (comportamiento):** `ValueError("El usuario U001 esta inactivo")` y
`ValueError("El recurso R0002 esta dado de baja")`; no se descuenta inventario.

**Archivos y funciones modificados:** `gestor_prestamos.py` → `registrar_prestamo` (líneas 86–100).

**Código ANTES:**
```python
        if self.gestor_usuarios:
            usuario = self.gestor_usuarios.buscar_por_codigo(usuario_codigo)
            if usuario is None:
                raise ValueError(f"Usuario {usuario_codigo} no existe")

        # Validar recurso si gestor_recursos está disponible
        if self.gestor_recursos:
            recurso = self.gestor_recursos.buscar_por_codigo(recurso_codigo)
            if recurso is None:
                raise ValueError(f"Recurso {recurso_codigo} no existe")
```
**Código DESPUÉS:**
```python
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
```

**Por qué se hizo así:** se reutilizan `Usuario.es_activo()` y `Recurso.obtener_estado()`, que ya
existían. Las validaciones van **antes** del descuento de inventario para que un préstamo rechazado no
reste unidades.
**Estructura de datos involucrada:** `VectorDinamico` de usuarios y `TablaHash` de recursos (búsquedas existentes).
**Requisito que satisface:** reglas de préstamo de M03 (coherente con RQF-004: un usuario dado de baja deja de operar).
**Salida — ANTES** (`evidencias/scripts/repro_e9_e11.py`; `evidencias/antes/E9_E10_E11.txt`):
```
E9: préstamo a usuario INACTIVO -> P0001
E9: préstamo de recurso DADO DE BAJA -> P0002
```
**Salida — DESPUÉS** (`evidencias/despues/E9_E10_E11.txt`):
```
E9: rechazado: El usuario U001 esta inactivo
E9: rechazado: El recurso R0002 esta dado de baja
```
**Prueba que lo verifica:** `test_e9_usuario_inactivo_recurso_baja`.

---

### E10 — El inventario no aceptaba más de 100 recursos

**Antes (comportamiento):** al registrar existencias del recurso 101 aparecía
`ValueError: No hay más espacio para recursos (máximo: 100)`, y el recurso quedaba registrado en
`GestorRecursos` pero sin columna en la matriz.
**Causa:** `GestorInventario.registrar_recurso` tenía un tope fijo (`num_recursos=100` desde `GestorRecursos`).
**Ahora (comportamiento):** cuando se llenan las columnas, la matriz duplica su número de columnas
copiando celda por celda, igual que el `VectorDinamico`. Acepta 500 recursos o más.

**Archivos y funciones modificados:** `modulos/M07_inventario/gestor_inventario.py` → método **nuevo**
`_redimensionar_columnas` (76–94) y `registrar_recurso` (96–115).

**Código ANTES:**
```python
    def registrar_recurso(self, codigo_recurso, nombre_recurso):
        """Registra un nuevo tipo de recurso. O(1)"""
        if self.contador_recursos >= self.num_recursos:
            raise ValueError(f"No hay más espacio para recursos (máximo: {self.num_recursos})")

        if codigo_recurso not in self.mapeo_recursos:
            idx = self.contador_recursos
```
**Código DESPUÉS:**
```python
    def _redimensionar_columnas(self):
        """
        Duplica el número de columnas de la matriz (misma estrategia que VectorDinamico).
        ...
        Complejidad: O(sedes × recursos) cuando ocurre. Como la capacidad se
        duplica, ocurre pocas veces (log n) y el registro queda en O(1) amortizado.
        """
        nueva_capacidad = max(1, self.num_recursos * 2)
        # Arreglo de bajo nivel de tamaño fijo por fila, igual que el que usa
        # VectorDinamico._redimensionar; no es una colección que crece con append.
        nueva_matriz = [[0] * nueva_capacidad for _ in range(self.num_sedes)]
        for i in range(self.num_sedes):
            for j in range(self.contador_recursos):
                nueva_matriz[i][j] = self.matriz[i][j]
        self.matriz = nueva_matriz
        self.num_recursos = nueva_capacidad

    def registrar_recurso(self, codigo_recurso, nombre_recurso):
        ...
        if codigo_recurso not in self.mapeo_recursos:
            # Antes se lanzaba ValueError aquí y el recurso 101 quedaba sin columna.
            if self.contador_recursos >= self.num_recursos:
                self._redimensionar_columnas()
            idx = self.contador_recursos
```

**Por qué se hizo así:** es la misma idea del `VectorDinamico`: duplicar la capacidad hace que el costo
de copiar se reparta entre muchos registros. Con 100 columnas iniciales, para 500 recursos la matriz
crece 3 veces (100 → 200 → 400 → 800). **Complejidad:** O(sedes × recursos) en el registro que provoca el
crecimiento y **O(1) amortizado** por registro. También se movió la verificación dentro del
`if codigo_recurso not in ...`: antes, con la matriz llena, ni siquiera se podía volver a consultar un
recurso ya registrado. La matriz sigue siendo un arreglo 2D de bajo nivel, como antes; `[0] * n` es el
mismo tipo de reserva de tamaño fijo que usa `VectorDinamico._redimensionar`.
**Estructura de datos involucrada:** matriz `[sede][recurso]` de `GestorInventario`.
**Requisito que satisface:** RNF (operar con al menos 500 registros), RQF-009.
**Salida — ANTES** (`evidencias/antes/E9_E10_E11.txt`):
```
E10: ValueError en el recurso 101 (R0101): No hay más espacio para recursos (máximo: 100)
     R0101 registrado en GestorRecursos: True; disponibilidad en la matriz: 0
```
**Salida — DESPUÉS** (`evidencias/despues/E9_E10_E11.txt`):
```
E10: 500 recursos OK; R0500 = 3
```
**Prueba que lo verifica:** `test_e10_inventario_500` (R0500 = 3, R0001 conserva 3 tras crecer, R0101
tiene columna, registrar de nuevo un código no crece la matriz, prestar R0101 descuenta).

---

### E11 — Deshacer un préstamo asignado desde la fila hacía perder el turno

**Antes (comportamiento):** si se deshacía el préstamo que se le había dado a U002 desde la fila, U002
desaparecía de la fila y su solicitud quedaba "Otorgado".
**Causa:** `registrar_prestamo` guardaba la `'solicitud'` en la pila, pero `deshacer` nunca la usaba;
`GestorTurnos.reinsertar_al_frente` ya existía y nadie lo llamaba.
**Ahora (comportamiento):** al deshacer ese préstamo, U002 vuelve al **primer** lugar de la fila y su
solicitud queda "En espera".

**Archivos y funciones modificados:** `gestor_prestamos.py` → `deshacer` (líneas 228–232).
`gestor_turnos.reinsertar_al_frente` no se modificó.

**Código ANTES:**
```python
            if _num(p.codigo) == self.contador_codigos:
                self.contador_codigos -= 1
        elif op['operacion'] == 'registrar_devolucion':
```
**Código DESPUÉS:**
```python
            if _num(p.codigo) == self.contador_codigos:
                self.contador_codigos -= 1

            # E11: si el préstamo se asignó desde la fila, el usuario no pierde su
            # turno: vuelve al frente y la solicitud queda otra vez "En espera".
            solicitud = op.get('solicitud')
            if solicitud is not None and self.gestor_turnos:
                self.gestor_turnos.reinsertar_al_frente(solicitud)
        elif op['operacion'] == 'registrar_devolucion':
```

**Por qué se hizo así:** deshacer debe dejar el sistema como estaba antes de la operación, y antes
del préstamo automático el usuario estaba primero en la fila. `reinsertar_al_frente` reconstruye la
cola poniéndolo adelante y llama a `solicitud.reiniciar()` ("En espera").

**Consecuencias en deshacer (comportamiento documentado):** con E4 y E6c, una devolución que asigna un
turno apila **dos** operaciones: primero la devolución y encima el préstamo automático.

| Paso | Pila (tope a la derecha) | Fila | Disponibilidad |
|---|---|---|---|
| U001 presta la única unidad (P0001) | [P0001] | [] | 0 |
| U002 y U003 piden turno | [P0001] | [U002, U003] | 0 |
| U001 devuelve → automático para U002 (P0002) | [P0001, dev P0001, P0002] | [U003] | 0 |
| **1.er deshacer**: revierte P0002 | [P0001, dev P0001] | **[U002, U003]** | 1 |
| **2.º deshacer**: revierte la devolución | [P0001] | [U002, U003] | 0 |

Esto está documentado en el docstring de `registrar_devolucion` y en el de `deshacer`. Las solicitudes de
usuarios inactivos que se saltaron (E6c) quedan "Cancelado" y no se restauran al deshacer.
**Estructura de datos involucrada:** `Pila` (deshacer) y `ColaFIFO` (reinsertar al frente).
**Requisito que satisface:** RF4 / RQF-015 (deshacer sin alterar el resto del historial) y RQF-016 (orden de llegada).
**Salida — ANTES** (`evidencias/antes/E9_E10_E11.txt`):
```
E11: cola antes  = ['U002', 'U003']
E11: atendido    = P0001 | cola = ['U003']
E11: tras deshacer cola = ['U003'] | estado S0001 = Otorgado
```
**Salida — DESPUÉS** (`evidencias/despues/E9_E10_E11.txt` y, desde el menú, `E6c_E11_extra.txt`):
```
E11: cola antes  = ['U002', 'U003']
E11: atendido    = P0001 | cola = ['U003']
E11: tras deshacer cola = ['U002', 'U003'] | estado S0001 = En espera
```
```
 Asignado automaticamente a U002 (siguiente en la fila): P0002
[...]
 Operacion deshecha (Pila LIFO)
[...]
Fila para R0003: 1 personas
[...]
Centro          | 5     | 2     | 1    
```
**Prueba que lo verifica:** `test_e11_deshacer_turno` (tabla de arriba completa,
`atender_siguiente_turno` directo, préstamo normal que no toca la fila, pila vacía).

---

## 5.3 Inventario de cambios en el código

| Tipo de cambio | Elemento | Archivo |
|---|---|---|
| Clase **nueva** | `SinUnidadesError(ValueError)` | `modulos/M03_prestamos/gestor_prestamos.py` |
| Método **nuevo** | `GestorPrestamos.listar_activos()` → `VectorDinamico` | `gestor_prestamos.py` |
| Parámetro **eliminado** | `exclusivo` de `GestorPrestamos.__init__` (y el atributo `self.exclusivo`) | `gestor_prestamos.py` |
| Método **modificado** | `registrar_prestamo`: valida usuario activo y recurso no dado de baja, descuenta 1 unidad, lanza `SinUnidadesError`; ya no devuelve `None` | `gestor_prestamos.py` |
| Método **modificado** | `registrar_devolucion`: suma 1 unidad, atiende la fila; ahora devuelve `False` / `True` / código del préstamo automático (antes `True`/`False`) | `gestor_prestamos.py` |
| Método **modificado** | `deshacer`: ±1 de inventario, reinserta al frente la solicitud, `ValueError` si no puede revertir una devolución | `gestor_prestamos.py` |
| Método **modificado** | `atender_siguiente_turno`: sin regla `exclusivo`, salta inactivos, reinserta si falla | `gestor_prestamos.py` |
| Método **modificado** (solo docstring) | `recurso_prestado`: ahora es informativo; **no se eliminó** | `gestor_prestamos.py` |
| Export **modificado** | `SinUnidadesError` agregado a `__all__` | `modulos/M03_prestamos/__init__.py` |
| Método **modificado** | `GestorTurnos.__init__(gestor_usuarios=None, gestor_recursos=None)` | `modulos/M04_turnos/gestor_turnos.py` |
| Método **nuevo** | `GestorTurnos.esta_en_espera(usuario, recurso)` | `gestor_turnos.py` |
| Método **nuevo** | `GestorTurnos.solicitar_turno(usuario, recurso, sede)` | `gestor_turnos.py` |
| Método **nuevo** | `GestorTurnos.ver_siguiente(recurso)` | `gestor_turnos.py` |
| Método **modificado** (solo docstring) | `GestorTurnos.obtener_siguiente`: aclara que desencola | `gestor_turnos.py` |
| Import **modificado** | `from estructuras import ArbolBinario, TablaHash` | `modulos/M05_categorias/gestor_categorias.py` |
| Atributo **modificado** | `GestorCategorias.categorias`: `dict` → `TablaHash(211)` | `gestor_categorias.py` |
| Método **modificado** | `registrar_categoria` (rechaza repetidos), `obtener_categoria` (`buscar`), `obtener_cantidad` (`obtener_cantidad`) | `gestor_categorias.py` |
| Método **nuevo** | `GestorInventario._redimensionar_columnas()` | `modulos/M07_inventario/gestor_inventario.py` |
| Método **modificado** | `GestorInventario.registrar_recurso`: sin tope, crece | `gestor_inventario.py` |
| Import **nuevo** | `from modulos.M03_prestamos import SinUnidadesError` | `main.py` |
| Función **nueva** | `solicitar_turno_menu(gestor_turnos, usuario, recurso, sede)` | `main.py` |
| Opción de menú **nueva** | Turnos → "4. Solicitar turno" | `main.py` |
| Opción de menú **modificada** | Turnos → 1 "Ver siguiente turno": usa `ver_siguiente` y muestra el código del turno | `main.py` |
| Opción de menú **modificada** | Préstamos → 1: `SinUnidadesError` ofrece pedir turno; `except Exception` → `except ValueError` | `main.py` |
| Opción de menú **modificada** | Préstamos → 2: revisa el retorno y muestra la asignación automática; `except Exception` → `except ValueError` | `main.py` |
| Opción de menú **modificada** | Préstamos → 3: usa `listar_activos()` (`VectorDinamico`) | `main.py` |
| Opción de menú **modificada** | Préstamos → 8: `try/except ValueError` | `main.py` |
| Opción de menú **modificada** | Usuarios → 1: `try/except ValueError` | `main.py` |
| Opción de menú **modificada** | Categorías → 1: `try/except ValueError` | `main.py` |
| Texto **modificado** | Menú principal, descripción del módulo 5: "Solicitar turno, ver turnos y fila de espera" | `main.py` |
| Construcción **modificada** | `main()`: `GestorTurnos(gestor_usuarios=..., gestor_recursos=...)` | `main.py` |
| Construcción **modificada** | `main()`: `GeneradorInformes(gestor_recursos=..., gestor_prestamos=...)` | `main.py` |
| Archivo **nuevo** | `pruebas/test_correcciones_menu.py` (13 pruebas, 99 casos) | — |
| Archivo **nuevo** | `CORRECCIONES.md` (este documento) | — |
| Archivo **nuevo** | `CAMBIOS.diff` | — |
| Carpeta **nueva** | `evidencias/` (salidas antes/después, salidas de pruebas, scripts de reproducción) | — |

**No se modificó:** `GestorUsuarios`, `GestorRecursos`, `GeneradorInformes`, `Solicitud`, `Prestamo`,
`reinsertar_al_frente`, las estructuras de `estructuras/`, `pruebas/test_basico.py`, `verificar_requisitos.py`.

---

## 5.4 Cambios de interfaz (lo que puede romper código de otros integrantes)

| # | Antes | Ahora | Archivos que lo usaban |
|---|---|---|---|
| 1 | `GestorPrestamos(gestor_turnos=None, exclusivo=True, gestor_usuarios=None, gestor_recursos=None)` | `GestorPrestamos(gestor_turnos=None, gestor_usuarios=None, gestor_recursos=None)` | `main.py` y `verificar_requisitos.py` usan argumentos con nombre → **no requieren cambios**. Quien pase `exclusivo=` recibe `TypeError`; quien pase el 2.º argumento por posición debe cambiarlo. |
| 2 | `registrar_prestamo(...)` devolvía el código **o `None`** | Devuelve siempre el código. Lanza `ValueError` (usuario inactivo, recurso dado de baja) o `SinUnidadesError` (sin unidades). **Con `gestor_recursos`, ahora exige unidades en la sede**: hay que cargar existencias con `actualizar_disponibilidad` antes de prestar | `main.py` (actualizado), `atender_siguiente_turno` (actualizado) |
| 3 | `registrar_devolucion(codigo)` → `True` / `False` | → `False` / `True` / `str` (código del préstamo automático) | `main.py` (actualizado) |
| 4 | `deshacer()` → `True` / `False` | Igual, pero puede lanzar `ValueError` si no puede revertir una devolución | `main.py` (actualizado) |
| 5 | `atender_siguiente_turno(recurso, sede)` → código o `None` | Igual, pero salta usuarios inactivos y, si falla el préstamo, reinserta y **relanza** el `ValueError` | `registrar_devolucion` (actualizado) |
| 6 | `GestorPrestamos.listar_activos()` no existía | Devuelve un **`VectorDinamico`**: usar `obtener_tamaño()` y `obtener(i)`, no `len()` ni `for p in ...` | `main.py` (actualizado) |
| 7 | `GestorTurnos()` | `GestorTurnos(gestor_usuarios=None, gestor_recursos=None)`; `GestorTurnos()` sigue funcionando | `main.py` (actualizado para pasar los gestores) |
| 8 | — | Métodos nuevos `solicitar_turno`, `ver_siguiente`, `esta_en_espera` | `main.py` |
| 9 | `registrar_categoria` aceptaba códigos repetidos; `gestor.categorias` era `dict` | Lanza `ValueError` si el código existe; `gestor.categorias` es `TablaHash` (usar `buscar`, no `[...]` ni `.get`) | `main.py` (actualizado); `verificar_requisitos.py` registra C1 una sola vez → sin cambios |
| 10 | `GestorInventario.registrar_recurso` lanzaba `ValueError` con más de `num_recursos` | Ya no lanza; `num_recursos` pasa a ser la **capacidad** actual de columnas y crece | `GestorRecursos` (sin cambios) |
| 11 | `GeneradorInformes(gestor_usuarios, gestor_recursos)` (llamada errónea) | `GeneradorInformes(gestor_recursos=..., gestor_prestamos=...)` | `main.py` (actualizado). La clase no cambió. |
| 12 | — | Excepción nueva `SinUnidadesError` (subclase de `ValueError`), exportada en `modulos.M03_prestamos` | `main.py` |

---

## 5.5 Cambios de comportamiento visibles en el menú

| Opción del menú | Antes mostraba | Ahora muestra |
|---|---|---|
| Usuarios → 1 con nombre vacío | `Traceback ... ValueError` (se cerraba) | `Error: El nombre del usuario no puede estar vacío` |
| Usuarios → 1 con email vacío | `Traceback ... ValueError` (se cerraba) | `Error: El email del usuario no puede estar vacío` |
| Préstamos → 1, segundo préstamo de R0001 en Centro | `Prestamo registrado: None` | `Prestamo registrado: P0002` |
| Préstamos → 1 sin unidades en la sede | `Prestamo registrado: None` | `Error: Sin unidades disponibles de R0003 en Centro` + `¿Desea pedir turno en la fila de espera? (s/n):` → `Turno S0001 asignado, posicion 1 en la fila` |
| Préstamos → 1 con usuario inactivo | `Prestamo registrado: P0002` | `Error: El usuario U001 esta inactivo` |
| Préstamos → 1 con recurso dado de baja | `Prestamo registrado: ...` | `Error: El recurso R0002 esta dado de baja` |
| Préstamos → 2 con P9999 | `Devolucion registrada` | `Error: El prestamo P9999 no existe o ya fue devuelto` |
| Préstamos → 2 con gente en la fila | `Devolucion registrada` (la fila no avanzaba) | `Devolucion registrada` + `Asignado automaticamente a U002 (siguiente en la fila): P0003` |
| Préstamos → 3 | `Traceback ... AttributeError` (se cerraba) | `Total prestamos activos: N` y la lista (`Total prestamos activos: 0` si no hay) |
| Préstamos → 8 cuando no se puede revertir una devolución | — | `Error: No se puede deshacer la devolucion de P0004: no quedan unidades de R0001 en Centro` |
| Inventario después de prestar/devolver | La matriz no cambiaba | La matriz descuenta/suma 1 en la sede |
| Turnos (lista de opciones) | 1–3 | Se agrega `4. Solicitar turno` |
| Turnos → 1 Ver siguiente | `Siguiente en fila: U002` **y lo sacaba de la fila** | `Siguiente en fila: U002 (turno S0001)` sin modificar la fila |
| Turnos → 4 Solicitar turno | (no existía) | `Turno S0001 asignado, posicion N en la fila`, o uno de: `Error: Hay unidades disponibles: registre el préstamo`, `Error: El usuario U002 ya esta en la fila de R0003`, `Error: Usuario U999 no existe`, `Error: El usuario U001 esta inactivo`, `Error: Recurso R0099 no existe`, `Error: El recurso R0002 esta dado de baja`, `Error: Sede 'Marte' no existe` |
| Categorías → 1 con código repetido | `Categoria registrada: C1` (sobrescribía) | `Error: La categoria C1 ya existe` |
| Informes → 1 Reporte de uso | `Total de préstamos registrados: 3` (eran recursos) | `Total de préstamos registrados: 1` (préstamos reales) |
| Informes → 2 Reporte de inventario | `GestorUsuarios(total=2, activos=2)` | `GestorRecursos(libros=1, equipos=1, salas=1)` |
| Menú principal, módulo 5 | `Ver turnos y fila de espera` | `Solicitar turno, ver turnos y fila de espera` |

---

## 5.6 Diff completo

Está en **`CAMBIOS.diff`** (`diff -u` del original contra el corregido): `main.py`,
`modulos/M03_prestamos/__init__.py`, `modulos/M03_prestamos/gestor_prestamos.py`,
`modulos/M04_turnos/gestor_turnos.py`, `modulos/M05_categorias/gestor_categorias.py`,
`modulos/M07_inventario/gestor_inventario.py` y el archivo nuevo `pruebas/test_correcciones_menu.py`.

---

## 5.7 Pruebas y trazabilidad

### Resultados

| Comando | Resultado |
|---|---|
| `python -m pruebas.test_basico` | **8/8** aprobadas (igual que antes) |
| `python -m pruebas.test_correcciones_menu` | **13/13** pruebas, **99 casos**, 0 fallidos |
| `python verificar_requisitos.py` | Sin `✗` |
| 7 comandos de la sección 3 | Los 7 terminan con `exit=0`, **ningún `Traceback`** (`evidencias/despues/`) |
| Comandos extra (pedir turno; devolver con fila + deshacer) | `exit=0`, sin `Traceback` |

### Casos obligatorios

| Caso | Resultado esperado | Prueba | Resultado |
|---|---|---|---|
| R0001 tiene 5 en Centro; se prestan 5 | Los 5 se registran y la disponibilidad queda en 0 | `test_e3`, `test_e4` | ✅ |
| Sexto préstamo | `ValueError` "Sin unidades disponibles…" | `test_e3` | ✅ (`SinUnidadesError`, subclase de `ValueError`) |
| Devolver uno | Disponibilidad en 1 | `test_e4` | ✅ |
| Deshacer esa devolución | Disponibilidad en 0 | `test_e4` | ✅ |
| Deshacer un préstamo | Disponibilidad +1 | `test_e4` | ✅ |
| Devolución con cola [U002, U003] | Préstamo automático para U002, cola [U003] | `test_e6c`, `test_e11` | ✅ |
| Deshacer ese préstamo automático | Cola [U002, U003] y U002 "En espera" | `test_e11` | ✅ |
| Deshacer otra vez | Se revierte la devolución original | `test_e11` | ✅ |
| Solicitar turno con unidades disponibles | Rechazado | `test_e6a` | ✅ |
| Solicitar turno dos veces (mismo usuario y recurso) | El segundo se rechaza | `test_e6a` | ✅ |
| `ver_siguiente` | No cambia el tamaño de la cola | `test_e6b` | ✅ |
| Préstamo a usuario inactivo | Rechazado | `test_e9` | ✅ |
| Préstamo de recurso dado de baja | Rechazado | `test_e9` | ✅ |
| Categoría repetida | Rechazada; nombre original conservado | `test_e7` | ✅ |
| 500 recursos con existencias | Sin errores; R0500 = 3; R0001 conserva su valor | `test_e10` | ✅ |
| `GeneradorInformes` | El reporte de uso cuenta préstamos, no recursos | `test_e8` | ✅ |

Cada caso se imprime como **ENTRADA → OPERACIÓN → RESULTADO ESPERADO → RESULTADO OBTENIDO**, por ejemplo:

```
  [error] ✅
    ENTRADA:            R0001 con 0 en Centro
    OPERACIÓN:          sexto préstamo
    RESULTADO ESPERADO: SinUnidadesError: Sin unidades disponibles de R0001 en Centro
    RESULTADO OBTENIDO: SinUnidadesError: Sin unidades disponibles de R0001 en Centro
```

La salida completa (572 líneas) está en `evidencias/salida_test_correcciones_menu.txt`.

<details>
<summary>Salida completa de <code>python -m pruebas.test_basico</code></summary>

```
======================================================================
PRUEBAS BÁSICAS — ENTREGA 1
======================================================================

🧪 TEST 1: Vector Dinámico
--------------------------------------------------
✅ Vector Dinámico: CORRECTO

🧪 TEST 2: Lista Simple
--------------------------------------------------
✅ Lista Simple: CORRECTO

🧪 TEST 3: Lista Doble
--------------------------------------------------
✅ Lista Doble: CORRECTO

🧪 TEST 4: Pila (LIFO)
--------------------------------------------------
✅ Pila: CORRECTO

🧪 TEST 5: Cola FIFO
--------------------------------------------------
✅ Cola FIFO: CORRECTO

🧪 TEST 6: Herencia (Recurso → Libro, Equipo, Sala)
--------------------------------------------------
✅ Herencia: CORRECTO

🧪 TEST 7: M01 - Gestor de Usuarios
--------------------------------------------------
✅ Gestor de Usuarios: CORRECTO

🧪 TEST 8: M02 - Gestor de Recursos
--------------------------------------------------
✅ Gestor de Recursos: CORRECTO

======================================================================
RESUMEN
======================================================================
✅ CORRECTO: Vector Dinámico
✅ CORRECTO: Lista Simple
✅ CORRECTO: Lista Doble
✅ CORRECTO: Pila
✅ CORRECTO: Cola FIFO
✅ CORRECTO: Herencia
✅ CORRECTO: Gestor Usuarios (M01)
✅ CORRECTO: Gestor Recursos (M02)

Total: 8/8 pruebas aprobadas

🎉 ¡TODAS LAS PRUEBAS PASARON!
```
</details>

<details>
<summary>Resumen de <code>python -m pruebas.test_correcciones_menu</code></summary>

```
======================================================================
RESUMEN
======================================================================
✅ CORRECTO: E1  Listar préstamos activos
✅ CORRECTO: E2  ValueError capturados en el menú
✅ CORRECTO: E3  Préstamo según unidades de la sede
✅ CORRECTO: E4  Inventario en préstamo/devolución/deshacer
✅ CORRECTO: E5  Devolución inexistente
✅ CORRECTO: E6a Solicitar turno
✅ CORRECTO: E6b Ver siguiente sin sacar
✅ CORRECTO: E6c Atender la fila al devolver
✅ CORRECTO: E7  Categoría repetida
✅ CORRECTO: E8  Informes
✅ CORRECTO: E9  Usuario inactivo / recurso de baja
✅ CORRECTO: E10 500 recursos en inventario
✅ CORRECTO: E11 Deshacer préstamo desde la fila

Total: 13/13 pruebas aprobadas

🎉 ¡TODAS LAS PRUEBAS PASARON!
```
</details>

---

## Observaciones fuera del alcance (no se tocaron)

1. **Codificación en Windows** (ver la nota del inicio): con la salida redirigida, `main.py` falla con
   `UnicodeEncodeError` por el carácter `═`. Ya ocurría antes de estas correcciones. Una solución de una
   línea sería `sys.stdout.reconfigure(encoding="utf-8")` al inicio de `main()`.
2. **`modulos/M02_recursos/inventario.py`** (clase `Inventario`) es un duplicado de `GestorInventario` que el
   programa no usa y conserva el tope de 100. Conviene eliminarlo o corregirlo igual que E10.
3. Siguen existiendo colecciones de Python **anteriores a este cambio**: `mapeo_recursos`/`mapeo_sedes` (`dict`)
   en `GestorInventario`, `codigos_usados` (`set`) en `GestorUsuarios` y `GestorRecursos`, `historial_prestamos`
   (`list`) en `Usuario`, `listar_sedes()` (devuelve `list`) y la reconstrucción con lista por comprensión en
   `GestorPrestamos.deshacer`. Conviene migrarlas a estructuras propias en la E2.
4. `estructuras/arbol_binario.py:25` muestra un `SyntaxWarning` (`"\ "` en el docstring) la primera vez que se
   compila. No es un error; se quita usando `r"""..."""`.
5. El menú no tiene opciones para dar de baja usuarios o recursos, por eso E9 se verifica con pruebas y no desde el menú.
6. La fila de espera es **por recurso** (no por sede): la unidad devuelta en una sede se presta, en esa misma
   sede, al primero de la fila. Si se suben existencias a mano con `actualizar_disponibilidad`, la fila no se
   atiende automáticamente (solo al devolver).
