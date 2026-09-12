"""Quien dejo sus datos.

Es lo unico que este sitio guarda, y por eso es lo unico que no puede fallar
(principio III). Un contacto perdido es un cliente perdido, y lo peor es que no
hay forma de enterarse de que se perdio.

El telefono es la llave (decision D-01). En este publico mucha gente no tiene
correo o no lo revisa, y el telefono es lo que de verdad identifica a un
comercio. Se guarda normalizado para que `0414-123.45.67` y `04141234567` sean
el mismo, que es lo que cualquiera esperaria.
"""

from django.conf import settings
from django.db import models


class EstadoContacto(models.TextChoices):
    NUEVO = "nuevo", "Sin atender"
    ATENDIDO = "atendido", "Ya le escribimos"
    CONVERTIDO = "convertido", "Abrio su tienda"
    DESCARTADO = "descartado", "No era para nosotros"


def solo_digitos(telefono):
    """El telefono, sin espacios, guiones ni puntos."""
    return "".join(c for c in (telefono or "") if c.isdigit())


class Contacto(models.Model):
    nombre = models.CharField("como se llama", max_length=120)
    comercio = models.CharField("como se llama su negocio", max_length=120)
    telefono = models.CharField("telefono", max_length=25)
    correo = models.EmailField("correo", max_length=254, blank=True)
    mensaje = models.TextField("lo que escribio", blank=True)

    # Desde que parte de la pagina pulso el boton. Dice que fue lo que lo
    # convencio, que es la unica forma de saber que seccion esta sirviendo.
    origen = models.CharField("desde donde escribio", max_length=40, blank=True)
    origen_ip = models.GenericIPAddressField(null=True, blank=True)

    estado = models.CharField(
        max_length=12, choices=EstadoContacto.choices, default=EstadoContacto.NUEVO
    )
    notas = models.TextField("notas nuestras", blank=True)

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    atendido_en = models.DateTimeField(null=True, blank=True)
    atendido_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contactos_atendidos",
    )

    class Meta:
        verbose_name = "contacto"
        verbose_name_plural = "contactos"
        ordering = ["-creado_en"]
        constraints = [
            # Quien manda el formulario y no ve respuesta en una hora, lo manda
            # otra vez. Eso no es un error suyo: es lo normal.
            models.UniqueConstraint(fields=["telefono"], name="un_contacto_por_telefono"),
        ]
        indexes = [
            models.Index(fields=["estado", "-creado_en"], name="contacto_estado_idx"),
        ]

    def __str__(self):
        return f"{self.nombre} — {self.comercio}"

    def save(self, *args, **kwargs):
        self.telefono = solo_digitos(self.telefono)
        super().save(*args, **kwargs)

    @property
    def esta_sin_atender(self):
        return self.estado == EstadoContacto.NUEVO

    @property
    def telefono_legible(self):
        """`04141234567` se lee mejor como `0414-1234567`."""
        numero = self.telefono
        if len(numero) == 11:
            return f"{numero[:4]}-{numero[4:]}"
        return numero
