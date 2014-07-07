# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext

from venta.apps.principal.models import *
from venta.apps.carrito.models import *
from venta.apps.principal.forms import *
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required,permission_required
from django.db.models import Q
#========================= importacion para pdf======================
import StringIO
#from xhtml12pdf import pisa
from xhtml2pdf import pisa
from  django.template.loader import render_to_string


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
            return HttpResponseRedirect('/productos_lista/')
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

def lista_por_categorias(request, categoria):
    listado=producto.objects.filter(nom_categoria__id= categoria)
    return render_to_response("lista_productos_categorias.html",{'lista':listado}, RequestContext(request))





@permission_required('principal.change_producto',login_url='/')
def update_produc(request, id_prod):
    if request.user.is_authenticated():
        productos = get_object_or_404(producto, pk=id_prod)
        stocks=get_object_or_404(stock,pk=id_prod)
        if request.method == 'POST':
            formulario = ProductoForm(request.POST, request.FILES, instance=productos)
            formulariostock=StockForm(request.POST,request.FILES,instance=stocks)

            if formulario.is_valid() and formulariostock.is_valid():
                formulario.save()
                formulariostock.save()
                return HttpResponseRedirect('/productos_lista/')
        else:
            formulario = ProductoForm(instance=productos)
            formulariostock=StockForm(instance=stocks)

        return render_to_response('update_produc.html', {'formulario': formulario,'formulariostock':formulariostock},context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')



def buscarProducto(request):
    if request.method=='POST':
        form=buscarProForm(request.POST)
        if form.is_valid():
            criterio=request.POST["buscar"]
            if criterio!="":
                data=criterio.split()
                if len(data)>1:
                    lista1=list(producto.objects.filter(Q(nombre_pro__contains=data[0])))
                    if len(lista1)==0:
                        lista1=list(producto.objects.filter(Q(nombre_pro__contains=data[1])))
                    return render_to_response('resultados.html',{'lista1':lista1},RequestContext(request))
                else:
                    lista=producto.objects.filter(Q(nombre_pro__contains=criterio))
            return render_to_response('resultados.html',{'lista':lista},RequestContext(request))
    form=buscarProForm()
    return render_to_response('base.html',{'formbuscar':form},RequestContext(request))

#====================== VISTAS PARA GENERAR PDF===========================================
@login_required(login_url='/login')
def crearReporte(request):
    productos = producto.objects.filter(estado=True)
    sto = stock.objects.all()
    html=render_to_string('reportesPDF/reporteproduc.html',{'pagesize':'A4','productos':productos,'stock': sto},context_instance=RequestContext(request))
    return generar_pdf(html)

def generar_pdf(html):
    resultado=StringIO.StringIO()
    pdf=pisa.pisaDocument(StringIO.StringIO(html.encode("UTF:8")),resultado)
    if not pdf.err:
        return HttpResponse(resultado.getvalue(),mimetype='application/pdf')
    return HttpResponse("Error en generar el pdf")


def reporteFiltro(request):
    if request.method=="POST":
        tipo=request.POST["sopcion"]
        if tipo=="1":
            f=request.POST["tfecha"]
            #return HttpResponse(fecha)
            busqueda=(
                    Q(fecha__icontains=f ))
            usuarios=perfil_user.objects.all()
            ventas= Pedido.objects.filter(busqueda)
            #print  ventas
            #return HttpResponse(ventas.count)
            html=render_to_string("reporvetans.html",{'pagesize':'A4','ventas':ventas,'usuarios':usuarios},context_instance=RequestContext(request))
            return generar_pdf(html)
        if tipo=="2":
            ventas= Pedido.objects.all()
            usuarios=perfil_user.objects.all()
            html=render_to_string("reporvetans.html",{'pagesize':'A4','ventas':ventas,'usuarios':usuarios},context_instance=RequestContext(request))
            return generar_pdf(html)
        if tipo=="3":
            usuarios=perfil_user.objects.all()
            ventas= Pedido.objects.all()
            html=render_to_string("reporvetans.html",{'pagesize':'A4','ventas':ventas,'usuarios':usuarios},context_instance=RequestContext(request))
            return generar_pdf(html)
    else:
        return HttpResponse("Error")


