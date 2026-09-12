"""El formulario publico, con su trampa para robots.

Es la unica superficie del sitio abierta a internet sin autenticar. Pide cuatro
cosas y no doce: cada campo de mas es gente que abandona a mitad.
"""

from django import forms

from .models import solo_digitos


class FormularioDeContacto(forms.Form):
    nombre = forms.CharField(
        label="Como se llama",
        max_length=120,
        widget=forms.TextInput(attrs={"autocomplete": "name", "placeholder": "Maria Perez"}),
    )
    comercio = forms.CharField(
        label="Como se llama su negocio",
        max_length=120,
        widget=forms.TextInput(
            attrs={"autocomplete": "organization", "placeholder": "Bodega La Esquina"}
        ),
    )
    telefono = forms.CharField(
        label="Su telefono",
        max_length=25,
        # El teclado numerico, que es lo que hace que se llene con una mano.
        widget=forms.TextInput(
            attrs={"inputmode": "tel", "autocomplete": "tel", "placeholder": "0414 1234567"}
        ),
        help_text="Por aqui le escribimos.",
    )
    correo = forms.EmailField(
        label="Su correo",
        required=False,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
        help_text="Opcional.",
    )
    mensaje = forms.CharField(
        label="Cuentenos algo de su negocio",
        required=False,
        widget=forms.Textarea(attrs={"rows": 2, "placeholder": "Opcional"}),
    )

    # La trampa. Nombre creible para un robot, invisible para una persona, fuera
    # del recorrido del teclado y anunciada a los lectores de pantalla como lo
    # que es. Un campo vacio que llega lleno solo pudo llenarlo un programa.
    sitio_web = forms.CharField(
        label="No llene este campo",
        required=False,
        widget=forms.TextInput(
            attrs={"autocomplete": "off", "tabindex": "-1", "aria-hidden": "true"}
        ),
    )

    def clean_telefono(self):
        numero = solo_digitos(self.cleaned_data["telefono"])
        if len(numero) < 10:
            raise forms.ValidationError(
                "Escriba el telefono completo, con el codigo. Por ejemplo: 0414 1234567."
            )
        if len(numero) > 15:
            raise forms.ValidationError("Ese telefono tiene demasiados numeros.")
        return numero

    def clean_nombre(self):
        valor = self.cleaned_data["nombre"].strip()
        if len(valor) < 2:
            raise forms.ValidationError("Escriba su nombre.")
        return valor

    def clean_comercio(self):
        valor = self.cleaned_data["comercio"].strip()
        if len(valor) < 2:
            raise forms.ValidationError("Escriba el nombre de su negocio.")
        return valor

    @property
    def lo_lleno_un_robot(self):
        """La trampa cayo. Se responde como a un envio bueno, y no se guarda."""
        return bool(self.data.get("sitio_web"))

    @property
    def campos_visibles(self):
        """Todos menos la trampa: la plantilla la dibuja aparte y escondida."""
        return [campo for campo in self if campo.name != "sitio_web"]
