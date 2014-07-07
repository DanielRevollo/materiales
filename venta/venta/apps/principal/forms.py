from django.forms import ModelForm
from django import forms
from venta.apps.principal.models import *
#las 3 clases siguienten son de los productos

class CategoriaForm(ModelForm):
    class Meta:
        model=categoria


class StockForm(ModelForm):
    class Meta:
        model=stock
        exclude = ['reg_pro']


class ProductoForm(ModelForm):
    class Meta:
        model=producto


class buscarProForm(forms.Form):
	buscar=forms.CharField(max_length=200)
