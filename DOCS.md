# docs.md — Aplicación 2: Entorno, configuración y buenas prácticas en Django

Proyecto: **entorno_config_django**  
Aplicación: **configuracion**

Este documento describe **qué hace cada parte del proyecto y por qué existe**, siguiendo exactamente lo que fue implementado.

---

## 1. Estructura general del proyecto

```

entorno_config_django/
├─ venv/
├─ entorno_config_django/
│  ├─ entorno_config_django/
│  │  ├─ settings.py
│  │  ├─ urls.py
│  │  └─ ...
│  ├─ configuracion/
│  │  ├─ models.py
│  │  ├─ views.py
│  │  ├─ urls.py
│  │  └─ ...
│  ├─ templates/
│  │  ├─ base.html
│  │  └─ configuracion/
│  │     ├─ home.html
│  │     ├─ entorno.html
│  │     └─ db.html
│  └─ manage.py

```

La estructura separa claramente:

- Configuración global del proyecto
- Lógica de la aplicación
- Templates reutilizables
- Entorno virtual aislado

---

## 2. Entorno virtual (`venv`)

El entorno virtual contiene **todas las dependencias del proyecto**.

Características:
- Aísla Django y sus librerías de otros proyectos
- Permite usar versiones específicas de Django
- Evita conflictos con instalaciones globales
- Hace el proyecto reproducible

Dentro del entorno virtual:
- `python`
- `pip`
- `django`
pertenecen **solo a este proyecto**

---

## 3. Proyecto Django (`entorno_config_django`)

El proyecto representa la **configuración global** de la aplicación web.

### `settings.py`

Archivo central de configuración.

En este proyecto se usa para:
- Registrar aplicaciones (`INSTALLED_APPS`)
- Definir templates globales (`TEMPLATES['DIRS']`)
- Centralizar configuración del entorno

El proyecto **no contiene lógica de negocio**, solo configuración.

---

### `urls.py` (proyecto)

Responsabilidad:
- Definir el **enrutador principal**
- Delegar rutas a las aplicaciones

Aquí se conecta la app `configuracion` al proyecto.

Flujo:
```

URL → urls.py (proyecto) → urls.py (app) → view

```

---

## 4. Aplicación `configuracion`

La app representa un **módulo funcional independiente**.

Su objetivo es mostrar:
- Configuración
- Entorno
- ORM
- Buenas prácticas

---

### `configuracion/urls.py`

Define las rutas internas de la app:

- `/` → home
- `/entorno/` → entorno
- `/db/` → base de datos

Este archivo desacopla rutas del proyecto principal.

---

## 5. Vistas (`views.py`)

Las vistas son el **controlador lógico** del patrón MTV.

### `home`

- Renderiza una página índice
- No accede a base de datos
- Solo entrega contexto básico al template

---

### `entorno`

- Lee configuración persistida en base de datos
- Demuestra centralización de configuración
- Expone variables al template

Conceptos involucrados:
- Separación de configuración y presentación
- Lectura de datos desde modelos
- Uso de contexto en renderización

---

### `db`

- Usa el ORM de Django
- Inserta datos automáticamente
- Consulta datos persistidos
- Devuelve resultados al template

Demuestra:
- Persistencia en SQLite
- ORM sin SQL explícito
- Migraciones funcionando

---

## 6. Modelos (`models.py`)

Los modelos representan la **capa de datos**.

---

### `AppSetting`

Modelo de configuración persistida.

Propósito:
- Centralizar valores de configuración
- Evitar hardcodear valores en vistas
- Demostrar configuración reutilizable

Características:
- Singleton controlado (`get_singleton`)
- Simula variables como DEBUG y ALLOWED_HOSTS
- Persistido en SQLite

---

### `Registro`

Modelo simple de registro.

Propósito:
- Demostrar uso del ORM
- Mostrar persistencia real
- Facilitar pruebas de migraciones

Cada visita a `/db/` crea un registro nuevo.

---

## 7. Base de datos (SQLite)

Base de datos usada:
- SQLite (por defecto de Django)

Características:
- No requiere instalación adicional
- Ideal para desarrollo
- Integración automática con Django

Las migraciones:
- Crean tablas
- Versionan cambios del modelo
- Mantienen consistencia del esquema

---

## 8. Templates

Los templates representan la **capa de presentación**.

---

### `templates/base.html`

Template base reutilizable.

Responsabilidades:
- Estructura HTML común
- Navegación
- Estilos básicos
- Definición de bloques

Aplica:
- DRY (no repetir HTML)
- Herencia de templates

---

### `home.html`

- Hereda de `base.html`
- Página índice
- Navegación interna

---

### `entorno.html`

- Muestra datos dinámicos
- Usa variables de contexto
- Demuestra renderización de configuración

---

### `db.html`

- Usa `{% if %}` y `{% for %}`
- Renderiza listas de datos
- Muestra interacción ORM → template

---

## 9. DRY (Don’t Repeat Yourself)

Aplicado en:
- Template base compartido
- Centralización de configuración
- Reutilización de vistas y layouts
- Un solo punto de verdad para estilos y navegación

---

## 10. Flujo completo de una petición

Ejemplo: `/db/`

```

Navegador
↓
urls.py (proyecto)
↓
urls.py (configuracion)
↓
views.db
↓
models.Registro
↓
SQLite
↓
contexto
↓
template db.html
↓
HTTP Response

```

---

## 11. Entorno desarrollo vs ejecución

Este proyecto está en **modo desarrollo**:

- `DEBUG` activo (simulado)
- SQLite
- runserver
- Sin optimizaciones de producción

Permite:
- Iterar rápido
- Observar errores
- Analizar comportamiento interno

---

## 12. Qué demuestra el proyecto

- Preparación correcta de un entorno Django
- Uso de entornos virtuales
- Configuración centralizada
- Separación proyecto / app
- ORM y migraciones
- Templates y herencia
- DRY aplicado de forma práctica
- Flujo real de ejecución en Django

---

## 13. Alcance intencional

Este proyecto **no incluye**:
- Autenticación
- Formularios complejos
- APIs
- Producción real

El foco es:
> Entorno, configuración y buenas prácticas estructurales en Django.
