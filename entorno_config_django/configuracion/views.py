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
