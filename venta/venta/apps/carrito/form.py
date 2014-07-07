from django import forms
#encoding:utf-8
from django.forms import ModelForm
from django.db import models
from models import *
class CantidadForm(forms.Form):
    cantidad=forms.IntegerField(label='Registre la Cantidad')


class fcarrito(ModelForm):
    class Meta:
        model=Carrito
        exclude=['producto','id_sesion','estado']
