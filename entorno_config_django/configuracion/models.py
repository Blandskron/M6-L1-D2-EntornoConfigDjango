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
