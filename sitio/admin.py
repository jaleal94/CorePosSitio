"""Los contactos en el admin. El panel propio es el sitio para trabajar."""

from django.contrib import admin

from .models import Contacto


@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "comercio", "telefono_legible", "estado", "creado_en")
    list_filter = ("estado", "creado_en")
    search_fields = ("nombre", "comercio", "telefono", "correo")
    date_hierarchy = "creado_en"
    readonly_fields = ("creado_en", "actualizado_en", "origen", "origen_ip")
