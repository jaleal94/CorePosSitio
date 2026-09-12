from django.urls import path

from . import views

app_name = "sitio"

urlpatterns = [
    path("", views.portada, name="portada"),
    path("gracias/", views.gracias, name="gracias"),
    path("privacidad/", views.privacidad, name="privacidad"),
    # El panel. Solo para el personal.
    path("contactos/", views.panel, name="panel"),
    path("contactos/<int:pk>/", views.actualizar_contacto, name="actualizar_contacto"),
    path("contactos/exportar/", views.exportar, name="exportar"),
]
