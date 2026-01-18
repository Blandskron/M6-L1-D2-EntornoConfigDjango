# Aplicación 2 — Entorno, configuración y buenas prácticas en Django

**Proyecto:** `entorno_config_django`  
**App:** `configuracion`

---

## 1) Crear carpeta del proyecto y entrar

```bash
mkdir entorno_config_django
cd entorno_config_django
````

---

## 2) Crear y activar entorno virtual (venv)

### Windows (PowerShell)

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

---

## 3) Instalar Django

```bash
python -m pip install --upgrade pip
pip install django
```

---

## 4) Crear el proyecto (sin punto)

```bash
django-admin startproject entorno_config_django
```

---

## 5) Entrar a la carpeta donde está `manage.py`

```bash
cd entorno_config_django
```

---

## 6) Crear la aplicación

```bash
python manage.py startapp configuracion
```

---

## 7) Ejecutar migraciones base de Django

```bash
python manage.py migrate
```

---

## 8) Modificar `entorno_config_django/settings.py` (solo cambios)

Agregar la app:

```python
INSTALLED_APPS += [
    "configuracion",
]
```

Asegurar templates globales (dentro de `TEMPLATES[0]`):

```python
"DIRS": [BASE_DIR / "templates"],
```

---

## 9) Modificar `entorno_config_django/urls.py` (solo cambios)

Agregar imports y rutas:

```python
from django.urls import include, path

urlpatterns += [
    path("", include("configuracion.urls")),
]
```

---

## 10) Crear `configuracion/urls.py`

```python
from django.urls import path

from . import views

app_name = "configuracion"

urlpatterns = [
    path("", views.home, name="home"),
    path("entorno/", views.entorno, name="entorno"),
    path("db/", views.db, name="db"),
]
```

---

## 11) Modificar `configuracion/views.py` (archivo completo)

```python
from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import AppSetting, Registro


def home(request: HttpRequest) -> HttpResponse:
    """
    Página índice para navegar por la app.
    """
    return render(
        request,
        "configuracion/home.html",
        {
            "titulo": "Entorno, configuración y buenas prácticas",
        },
    )


def entorno(request: HttpRequest) -> HttpResponse:
    """
    Muestra información mínima del entorno de ejecución (dev).
    """
    config = AppSetting.get_singleton()

    return render(
        request,
        "configuracion/entorno.html",
        {
            "titulo": "Entorno y configuración",
            "debug": config.debug,
            "allowed_hosts": config.allowed_hosts,
            "version_app": config.version_app,
        },
    )


def db(request: HttpRequest) -> HttpResponse:
    """
    Demuestra uso básico del ORM + migraciones (SQLite).
    """
    # Crea un registro simple por visita (para ver persistencia en SQLite)
    Registro.objects.create(origen="visitadb")

    registros = Registro.objects.order_by("-creado_en")[:10]

    return render(
        request,
        "configuracion/db.html",
        {
            "titulo": "Soporte de base de datos (ORM + SQLite)",
            "total": Registro.objects.count(),
            "registros": registros,
        },
    )
```

---

## 12) Modificar `configuracion/models.py` (archivo completo)

```python
from __future__ import annotations

from django.db import models


class AppSetting(models.Model):
    """
    Configuración simple persistida en DB (ejemplo de centralización).
    """

    debug = models.BooleanField(default=True)
    allowed_hosts = models.CharField(
        max_length=255,
        default="",
        blank=True,
        help_text="Hosts permitidos (texto simple para demo).",
    )
    version_app = models.CharField(max_length=32, default="1.0.0")

    class Meta:
        verbose_name = "Configuración de la aplicación"
        verbose_name_plural = "Configuración de la aplicación"

    def __str__(self) -> str:
        return f"AppSetting(debug={self.debug}, version={self.version_app})"

    @classmethod
    def get_singleton(cls) -> "AppSetting":
        """
        Asegura una única fila de configuración.
        """
        obj, _ = cls.objects.get_or_create(id=1)
        return obj


class Registro(models.Model):
    """
    Registro mínimo para demostrar ORM y persistencia en SQLite.
    """

    origen = models.CharField(max_length=50)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Registro"
        verbose_name_plural = "Registros"
        ordering = ["-creado_en"]

    def __str__(self) -> str:
        return f"{self.origen} @ {self.creado_en}"
```

---

## 13) Crear carpetas de templates

### Windows (PowerShell/CMD)

```bash
mkdir templates
mkdir templates\configuracion
```

---

## 14) Crear `templates/base.html`

```html
<!doctype html>
<html lang="es">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <title>{% block title %}Django Config{% endblock %}</title>

    <style>
      body { font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; margin: 0; }
      header, main { max-width: 980px; margin: 0 auto; padding: 16px; }
      header { border-bottom: 1px solid #e5e7eb; }
      nav a { margin-right: 12px; text-decoration: none; }
      code, pre { background: #f3f4f6; padding: 2px 6px; border-radius: 6px; }
      .card { border: 1px solid #e5e7eb; border-radius: 12px; padding: 12px; margin: 12px 0; }
      .muted { color: #6b7280; }
    </style>
  </head>

  <body>
    <header>
      <div class="muted">Aplicación 2 — Entorno, configuración y buenas prácticas</div>
      <h1 style="margin: 8px 0;">{% block h1 %}Django Config{% endblock %}</h1>

      <nav>
        <a href="{% url 'configuracion:home' %}">Inicio</a>
        <a href="{% url 'configuracion:entorno' %}">Entorno</a>
        <a href="{% url 'configuracion:db' %}">DB</a>
      </nav>
    </header>

    <main>
      {% block content %}{% endblock %}
    </main>
  </body>
</html>
```

---

## 15) Crear `templates/configuracion/home.html`

```html
{% extends "base.html" %}

{% block title %}Inicio | Configuración{% endblock %}
{% block h1 %}Inicio{% endblock %}

{% block content %}
  <div class="card">
    <p><strong>{{ titulo }}</strong></p>
    <p class="muted">Rutas:</p>
    <ul>
      <li><code>/entorno/</code></li>
      <li><code>/db/</code></li>
    </ul>
  </div>
{% endblock %}
```

---

## 16) Crear `templates/configuracion/entorno.html`

```html
{% extends "base.html" %}

{% block title %}Entorno | Configuración{% endblock %}
{% block h1 %}Entorno{% endblock %}

{% block content %}
  <div class="card">
    <p><strong>DEBUG (persistido en DB):</strong> <code>{{ debug }}</code></p>
    <p><strong>ALLOWED_HOSTS (texto demo):</strong> <code>{{ allowed_hosts }}</code></p>
    <p><strong>Versión app:</strong> <code>{{ version_app }}</code></p>
  </div>

  <div class="card">
    <p class="muted">
      Nota: esta página lee una configuración simple desde el modelo <code>AppSetting</code>.
    </p>
  </div>
{% endblock %}
```

---

## 17) Crear `templates/configuracion/db.html`

```html
{% extends "base.html" %}

{% block title %}DB | Configuración{% endblock %}
{% block h1 %}DB (ORM + SQLite){% endblock %}

{% block content %}
  <div class="card">
    <p><strong>Total registros:</strong> <code>{{ total }}</code></p>
    <p class="muted">Se crea 1 registro por visita a <code>/db/</code>.</p>
  </div>

  <div class="card">
    <h3 style="margin-top:0;">Últimos 10</h3>

    {% if registros %}
      <ul>
        {% for r in registros %}
          <li>
            <strong>{{ r.origen }}</strong>
            <span class="muted">— {{ r.creado_en }}</span>
          </li>
        {% endfor %}
      </ul>
    {% else %}
      <p class="muted">Aún no hay registros.</p>
    {% endif %}
  </div>
{% endblock %}
```

---

## 18) Crear migraciones de la app y aplicar

```bash
python manage.py makemigrations configuracion
python manage.py migrate
```

---

## 19) Levantar el servidor

```bash
python manage.py runserver
```

Rutas:

* `http://127.0.0.1:8000/`
* `http://127.0.0.1:8000/entorno/`
* `http://127.0.0.1:8000/db/`

---

## 20) Guardar dependencias (opcional)

```bash
pip freeze > requirements.txt
```

---

## 21) Salir del entorno virtual

```bash
deactivate
```
