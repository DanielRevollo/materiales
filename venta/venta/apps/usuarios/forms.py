
from django.forms import ModelForm
from django import forms
from venta.apps.usuarios.models import *
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    passsword = forms.CharField(widget=forms.PasswordInput(render_value=False))


class perfil_userForm(ModelForm):
    class Meta:
        model= perfil_user
        exclude=['user','per_user']

#lo que isimos por el amail
class ContactoForm(forms.Form):
    Email=forms.EmailField(widget=forms.TextInput())
    Titulo=forms.CharField(widget=forms.TextInput())
    Texto=forms.CharField(widget=forms.Textarea())
#lo que isimos por el amail

class fusuario(forms.Form):
    username=forms.CharField(widget=forms.TextInput(),required=True)
    password=forms.CharField(widget=forms.PasswordInput(),required=True)