# CÓMO EJECUTAR EL PROYECTO — VERSIÓN STARTUP

## Para Sustentación (Profesora)

### Opción 1: DEMO INTERACTIVO COMPLETO (lo más importante)

```bash
# 1. Abrir terminal en la carpeta del proyecto
cd "D:\user\Downloads\Repo proyecto beta"

# 2. Ejecutar main.py
python main.py
```

**MENÚ EXPANDIDO (15+ opciones):**

```
═══════════════════════════════════════════════════════════
  SISTEMA DE GESTIÓN DE RECURSOS — Startup Edition
═══════════════════════════════════════════════════════════

OPERACIONES BÁSICAS (Entrega 1):
  1. Registrar usuario (M01 - VectorDinamico)
  2. Registrar recurso (M02 - HERENCIA)
  3. Registrar sede
  4. Consultar usuario
  5. Consultar recurso
  6. Mostrar inventario (MATRIZ)
  7. Registrar préstamo (M03)
  8. Listar usuarios
  9. Listar recursos
  10. Pruebas de estructuras (Vector, Listas, Pila, Cola)

FEATURES STARTUP (Opción C - Innovación):
  11. 🚀 M10: RECOMENDACIONES INTELIGENTES (IA)
  12. 🚀 M11: CALIFICACIONES Y REVIEWS (Community)
  13. 🚀 M12: PREDICCIÓN DE DISPONIBILIDAD (Analytics)
  14. 🚀 M13: GAMIFICACIÓN (Badges & Leaderboards)
  15. 🚀 Ver LEADERBOARDS

  0. Salir
```

**QUÉ VER EN CADA OPCIÓN:**

**ACADÉMICO (Entrega 1):**

1. **Opción 1**: Registrar usuario → demuestra **VectorDinamico**
   - Usa Vector en M01 para almacenar usuarios
   - Ver: `modulos/M01_usuarios/gestor_usuarios.py`

2. **Opción 2**: Registrar recurso → demuestra **HERENCIA**
   - Seleccionar 1, 2, 3 para Libro, Equipo, Sala
   - Ver archivos: `modulos/M02_recursos/`
   - `libro.py:class Libro(Recurso):`
   - `equipo.py:class Equipo(Recurso):`
   - `sala.py:class Sala(Recurso):`

3. **Opción 6**: Mostrar inventario → demuestra **MATRIZ**
   - Ver tabla [sede][recurso] = cantidad
   - Archivo: `modulos/M02_recursos/inventario.py`

4. **Opción 10**: Pruebas de estructuras → demuestra todas las lineales
   - VectorDinamico: crece de 2 a 4 cuando se llena
   - ListaSimple: [A, B, C]
   - ListaDoble: adelante [X,Y,Z] y atrás [Z,Y,X]
   - Pila: LIFO (últimos que entra es primero que sale)
   - Cola: FIFO (primero que entra es primero que sale)

**STARTUP INNOVADOR (Opción C):**

11. **Opción 11: M10 - Recomendaciones Inteligentes** 🤖
    - ¿QUÉ VER?
      * Registra algunos préstamos
      * Sistema sugiere recursos que usuarios "similares" pidieron
      * Basado en Collaborative Filtering (IA básica)
    - ARCHIVO: `modulos/M10_recomendaciones/motor_recomendaciones.py`
    - ALGORITMO: Jaccard Similarity (similitud entre usuarios)
    - DEMO: Ver cómo sistema aprende de historiales

12. **Opción 12: M11 - Calificaciones & Reviews** ⭐
    - ¿QUÉ VER?
      * Usuarios califican recursos (1-5 estrellas)
      * Escriben comentarios
      * Sistema genera RANKING de mejores recursos
      * Como Airbnb/Uber: comunidad vota
    - ARCHIVO: `modulos/M11_calificaciones/gestor_calificaciones.py`
    - DEMO: Ver ranking de recursos + reviews más útiles

13. **Opción 13: M12 - Predicción de Disponibilidad** 📈
    - ¿QUÉ VER?
      * Predice cuándo estará libre un recurso
      * Basado en histórico de préstamos
      * Sugiere MEJOR HORARIO (menos congestión)
    - ARCHIVO: `modulos/M12_predicciones/predictor_disponibilidad.py`
    - ANÁLISIS: Duración promedio + demanda por hora
    - DEMO: Predicción de fecha + hora recomendada

14. **Opción 14: M13 - Gamificación** 🏆
    - ¿QUÉ VER?
      * Usuarios ganan PUNTOS por acciones
      * Desbloquean BADGES (6 tipos: Leal, Devolvedor, etc.)
      * Suben NIVELES (1-10)
      * Ver LEADERBOARDS
    - ARCHIVO: `modulos/M13_gamificacion/gestor_gamificacion.py`
    - DEMO: 
      * Registrar acciones (préstamo, devolución, review)
      * Ver cómo suben puntos y se desbloquean badges
      * Ver resumen del usuario gamificado

15. **Opción 15: LEADERBOARDS** 🏅
    - ¿QUÉ VER?
      * Top 10 usuarios por puntos
      * Usuarios agrupados por NIVEL
      * Usuarios con cada BADGE
      * Estadísticas globales (promedio puntos, nivel, etc.)
    - DEMO: Ver rankings en vivo, competencia entre usuarios

---

### Opción 2: PRUEBAS AUTOMATIZADAS

```bash
cd "D:\user\Downloads\Repo proyecto beta"
python pruebas/test_basico.py
```

**Salida esperada:**
```
✅ Vector Dinámico: CORRECTO
✅ Lista Simple: CORRECTO
✅ Lista Doble: CORRECTO
✅ Pila: CORRECTO
✅ Cola FIFO: CORRECTO
✅ Herencia: CORRECTO
✅ Gestor de Usuarios: CORRECTO
✅ Gestor de Recursos: CORRECTO

🎉 ¡TODAS LAS PRUEBAS PASARON!
```

---

## Dónde Está Cada Cosa

### Estructuras de Datos Lineales (Entrega 1)

| Estructura | Archivo | Complejidad | Usado en |
|-----------|---------|------------|----------|
| **VectorDinamico** | `estructuras/vector_dinamico.py` | O(1) agregar amortizado | M01, M02 |
| **ListaSimple** | `estructuras/lista_simple.py` | O(n) búsqueda, O(1) insertar | M03 |
| **ListaDoble** | `estructuras/lista_doble.py` | O(n) búsqueda, O(1) insertar ambos extremos | M03 |
| **Pila** | `estructuras/pila.py` | O(1) push/pop | M03 (deshacer) |
| **ColaFIFO** | `estructuras/cola_fifo.py` | O(1) encolar/desencolar | M04 (turnos) |

### Herencia (Entrega 1)

```
modulos/M02_recursos/
├── recurso.py          ← Clase BASE (abstracta)
├── libro.py            ← class Libro(Recurso):
├── equipo.py           ← class Equipo(Recurso):
└── sala.py             ← class Sala(Recurso):
```

Ver línea donde dice `class Libro(Recurso):` para demostrar herencia.

### Módulos Principales

| Módulo | Archivo | Clase Principal | Estado |
|--------|---------|-----------------|--------|
| **M01** | `modulos/M01_usuarios/` | `GestorUsuarios` | ✅ Completo |
| **M02** | `modulos/M02_recursos/` | `GestorRecursos` | ✅ Completo |
| M03 | `modulos/M03_prestamos/` | `GestorPrestamos` | Funcional |
| M04 | `modulos/M04_turnos/` | `GestorTurnos` | Funcional |
| M05 | `modulos/M05_indices/` | `IndiceBusqueda` | Funcional |
| M06 | `modulos/M06_listados/` | `ListadosRecursos` | Funcional |
| M07 | `modulos/M07_categorias/` | `GestorCategorias` | Funcional |
| M08 | `modulos/M08_sedes/` | `GestorSedes` | Funcional |
| M09 | `modulos/M09_informes/` | `GeneradorInformes` | Funcional |

---

## Respuestas a Preguntas Esperadas

### P: ¿Dónde está la herencia?

**Respuesta:**
```
modulos/M02_recursos/
├── recurso.py
    class Recurso(ABC):         ← Clase BASE
        def es_disponible()
        def obtener_info()
        
├── libro.py
    class Libro(Recurso):       ← HEREDA de Recurso
        def __init__(..., autor, isbn, año_publicacion):
            super().__init__(...)
            
├── equipo.py
    class Equipo(Recurso):      ← HEREDA de Recurso
        def __init__(..., tipo_equipo, modelo, ubicacion):
            super().__init__(...)
            
└── sala.py
    class Sala(Recurso):        ← HEREDA de Recurso
        def __init__(..., capacidad, recursos_disponibles):
            super().__init__(...)
```

Ver: Abrir `modulos/M02_recursos/libro.py` línea `class Libro(Recurso):`

---

### P: ¿Dónde está el Vector Dinámico?

**Respuesta:**
1. Archivo: `estructuras/vector_dinamico.py`
2. Usado en M01: `modulos/M01_usuarios/gestor_usuarios.py` línea `self.usuarios = VectorDinamico(...)`
3. Usado en M02: `modulos/M02_recursos/gestor_recursos.py` línea `self.recursos = VectorDinamico(...)`
4. Demostración: Ejecutar `main.py` → Opción 10 → "1. VECTOR DINÁMICO"

Ver cómo se redimensiona automáticamente de capacidad 2 → 4.

---

### P: ¿Dónde está la Lista Simple?

**Respuesta:**
1. Archivo: `estructuras/lista_simple.py`
2. Usado en M03: `modulos/M03_prestamos/gestor_prestamos.py` línea `self.historial_simple = ListaSimple()`
3. Demostración: `main.py` → Opción 10 → "2. LISTA SIMPLE"

Estructura: cada nodo tiene dato + apuntador `siguiente`.

---

### P: ¿Dónde está la Lista Doble?

**Respuesta:**
1. Archivo: `estructuras/lista_doble.py`
2. Usado en M03 para historial bidireccional
3. Demostración: `main.py` → Opción 10 → "3. LISTA DOBLE"

Cada nodo tiene:
```python
self.dato = dato
self.siguiente = None
self.anterior = None  ← Permite navegar atrás
```

---

### P: ¿Dónde está la Matriz?

**Respuesta:**
1. Archivo: `modulos/M02_recursos/inventario.py`
2. Clase: `Inventario`
3. Estructura: `self.matriz = [[cantidad] para cada [sede][recurso]]`
4. Demostración: `main.py` → Opción 6 → muestra tabla

Ejemplo:
```
Sede\Recurso | R0001 | R0002 | R0003
Sede Centro  |   5   |   2   |   1
Sede Norte   |   0   |   0   |   0
Sede Sur     |   0   |   0   |   0
```

---

### P: ¿Cómo resuelven el caso concreto?

**Respuesta:**

**El caso**: Red de N sedes universitarias con 3 tipos de recursos (libros, equipos, salas)

**La solución**:
1. M01 (usuarios): Registra cuándo entra un usuario
2. M02 (recursos): Registra catálogo (usa HERENCIA para tipos)
3. M03 (préstamos): Ejecuta la transacción
4. M04 (turnos): Si no hay recurso, lo encola
5. M05-M09: Análisis y reportes

**Estructuras usadas**:
- **Vector**: almacenar sin límite previo
- **Listas**: historial de transacciones
- **Pila**: deshacer última operación
- **Cola**: turnos justos (FIFO)
- **Matriz**: disponibilidad por sede

---

## Requisitos Técnicos

```
Python 3.7+
No requiere librerías externas
```

Verificar:
```bash
python --version
```

---

## Estructura del Proyecto

```
D:\user\Downloads\Repo proyecto beta\
├── main.py                    ← Ejecutar aquí
├── README.md                  ← Documentación completa
├── ENTREGA1.md               ← Resumen de Entrega 1
├── COMO_EJECUTAR.md          ← Este archivo
│
├── estructuras/              ← Estructuras lineales
│   ├── vector_dinamico.py
│   ├── lista_simple.py
│   ├── lista_doble.py
│   ├── pila.py
│   └── cola_fifo.py
│
├── modulos/                  ← 9 módulos
│   ├── M01_usuarios/         ✅ Completo (VectorDinamico)
│   ├── M02_recursos/         ✅ Completo (Herencia + Matriz)
│   ├── M03_prestamos/        (Funcional)
│   ├── M04_turnos/           (Funcional)
│   └── ...
│
└── pruebas/
    └── test_basico.py        ← Ejecutar aquí para pruebas
```

---

## Pasos Recomendados para Sustentación

1. **Ejecutar main.py**
   ```bash
   python main.py
   ```
   Ver menú interactivo

2. **Opción 1**: Registrar 2-3 usuarios
   - Muestra VectorDinamico funcionando en M01

3. **Opción 2**: Registrar 1 Libro, 1 Equipo, 1 Sala
   - Muestra HERENCIA en acción (Recurso → Libro, Equipo, Sala)
   - Abrir archivo `modulos/M02_recursos/libro.py` en pantalla para mostrar código

4. **Opción 3**: Registrar una sede (ej: "Centro")

5. **Opción 6**: Mostrar inventario
   - Muestra MATRIZ [sede][recurso]

6. **Opción 10**: Pruebas de estructuras
   - Demuestra VectorDinamico, ListaSimple, ListaDoble, Pila, Cola

7. **Opción 0**: Salir

---

## Ejecución de Pruebas (Alternativa)

```bash
python pruebas/test_basico.py
```

Esto ejecuta 8 tests:
- Vector Dinámico
- Lista Simple
- Lista Doble
- Pila
- Cola FIFO
- Herencia
- Gestor Usuarios (M01)
- Gestor Recursos (M02)

Resultado esperado: ✅ TODAS LAS PRUEBAS PASARON

---

## Preguntas Técnicas Esperadas

**P: ¿Cuál es la complejidad del Vector Dinámico?**
A: O(1) amortizado. Cuando se llena, se duplica la capacidad (O(n)) pero esto ocurre logarítmicamente pocas veces.

**P: ¿Por qué Lista Simple y Doble?**
A: Simple para historial hacia adelante (M03). Doble para poder navegar atrás también (último préstamo, etc.).

**P: ¿Por qué Matriz para inventario?**
A: O(1) para consultar/actualizar disponibilidad. Alternativa sería búsqueda lineal (O(n)).

**P: ¿Qué pasa si se llena el Vector?**
A: Se redimensiona: duplica capacidad y copia elementos. Esto toma O(n) pero ocurre raramente.

---

## Contacto para Dudas

Revisar documentación en:
- `README.md` (general)
- `ENTREGA1.md` (específico de Entrega 1)
- Docstrings en cada archivo `.py`

Cada función tiene docstring con:
- Descripción
- Parámetros
- Retorno
- Complejidad
- Ejemplo de uso
