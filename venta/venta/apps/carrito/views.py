#Librerias para el http
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from django.contrib.auth.decorators import login_required
import datetime

#Importaciones de los models de carrito y produto
from venta.apps.carrito.models import *
from venta.apps.usuarios.models import *
from venta.apps.principal.models import *
from venta.apps.carrito.form import *



#def new_venta(request, venta_id=0):
#    if int(venta_id) == 0:
#        ven = Venta.objects.create(
#            cliente=request.user
#        )


def new_venta(request, venta_id=0):
    if int(venta_id) == 0:
        ven = Venta.objects.create(cliente=request.user)
    else:
        ven = Venta.objects.get(pk=venta_id)
    sto = stock.objects.all()
    productos = producto.objects.all()
    detalleventa = DetalleVenta.objects.filter(venta_id=ven.id)
    return render_to_response('carrito/new_venta.html',
                              {'productos': productos, 'stock': sto, 'detalleventa': detalleventa, 'venta': ven},
                              context_instance=RequestContext(request))


def new_cantidad(request, id_venta, id_pro):
    if request.method == 'POST':
        formulario = CantidadForm(request.POST)
        if formulario.is_valid():
            cant = request.POST['cantidad']
            prod = producto.objects.get(pk=id_pro)
            costo = float(cant) * prod.Precio
            DetalleVenta.objects.create(
                cantidad=cant,
                costo_producto=costo,
                producto=prod,
                venta_id=id_venta,
            )
            vent = Venta.objects.get(pk=id_venta)
            vent.costo_total = vent.costo_total + costo
            vent.save()
            sto = stock.objects.get(reg_pro_id=id_pro)
            sto.cantidad = sto.cantidad - int(cant)
            sto.save()
            return HttpResponseRedirect('/carrito/new/' + str(id_venta) + '/')
    else:
        formulario = CantidadForm()
    return render_to_response('carrito/cantidad.html', {'formulario': formulario},
                              context_instance=RequestContext(request))


def confirmar(request, id_venta, ):
    ven = get_object_or_404(Venta, pk=id_venta)
    ven.estado = True
    ven.save()
    return HttpResponseRedirect('/')
