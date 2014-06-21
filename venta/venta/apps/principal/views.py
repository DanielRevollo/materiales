# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext

from venta.apps.principal.models import *
from venta.apps.principal.forms import *
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required,permission_required

def home(request):
    return render_to_response('base.html', context_instance=RequestContext(request))

#========================== tablas de procdustos===============================

@permission_required('principal.add_categoria',login_url='/')
def new_categ(request):#esta funcion devuelve el formulario creado en form.py
    if request.method == 'POST':
        formulario = CategoriaForm(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/categorias')# nos nmanda al index
    else:
        formulario = CategoriaForm()
    return render_to_response('new_categ.html', {'formulario': formulario}, context_instance=RequestContext(request))

def new_stock(request):
    if request.method == 'POST':
        formulario = StockForm(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/stock')# nos nmanda al index
    else:
        formulario = StockForm()
    return render_to_response('new_produc.html', {'formulario': formulario}, context_instance=RequestContext(request))

@permission_required('principal.add_producto',login_url='/')
def create_producto(request):
    if request.method == 'POST':
        formularioproducto = ProductoForm(request.POST, request.FILES)
        formulariostock = StockForm(request.POST)
        if formularioproducto.is_valid() and formulariostock.is_valid():
            pro = formularioproducto.save()
            stock = formulariostock.save()
            stock.reg_pro=pro
            stock.save()
            return HttpResponseRedirect('/')
    else:
        formularioproducto = ProductoForm()
        formulariostock = StockForm()
    return render_to_response('new_produc.html', {'formularioproducto':formularioproducto, 'formulariostock':formulariostock}, context_instance=RequestContext(request))

#=========================== tablas de productos===========================================================
@permission_required('principal.add_categoria',login_url='/')
def lista_categorias(request):
    categorias = categoria.objects.all()
    return render_to_response('lista_categorias.html', {'lista': categorias}, context_instance=RequestContext(request))

def lista_productos(request):
    productos = producto.objects.filter(estado=True)
    return render_to_response('lista_producto.html', {'lista': productos}, context_instance=RequestContext(request))




@permission_required('principal.change_producto',login_url='/')
def update_produc(request, id_prod):
    if request.user.is_authenticated():
        productos = get_object_or_404(producto, pk=id_prod)
        if request.method == 'POST':
            formulario = ProductoForm(request.POST, request.FILES, instance=productos)

            if formulario.is_valid():
                formulario.save()
                return HttpResponseRedirect('/productos/')
        else:
            formulario = ProductoForm(instance=productos)
        return render_to_response('update_produc.html', {'formulario': formulario},context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')
