from django.shortcuts import render


def portada(request):
    return render(request, "sitio/portada.html")
