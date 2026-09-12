from django.contrib import admin
from django.urls import include, path

# Paginas de error propias: quien las lee es una comerciante, no una
# programadora.
handler404 = "sitio.views.no_encontrado"
handler500 = "sitio.views.fallo_del_servidor"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("sitio.urls")),
]
