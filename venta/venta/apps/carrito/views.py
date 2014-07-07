from django.shortcuts import render, render_to_response,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext

from django.contrib.auth.decorators import login_required,permission_required
from venta.apps.principal.models import *
from venta.apps.usuarios.models import *
from django.db.models import Q

from form import *
import hashlib
import datetime
#==============REPORTES=======================
import StringIO
#from xhtml12pdf import pisa
from xhtml2pdf import pisa
from django.template.loader import render_to_string

#======================================
@login_required(login_url='/login')
def productos(request):
    lista_productos = producto.objects.all()
    return render_to_response("carrito/productos.html", {'lista_productos': lista_productos},
                              context_instance=RequestContext(request))

@login_required(login_url='/login')
def carrito_mostrar(request):
    if not "contador" in request.session:
        request.session['contador'] = 0
    return HttpResponse(request.session['contador'])

@login_required(login_url='/login')
def cargar_carrito(request, id):
    pro = producto.objects.get(id=int(id))
    fcarr = fcarrito()
    return render_to_response("carrito/fcarrito.html", {'fcarr': fcarr, 'pro': pro},
                              context_instance=RequestContext(request))

@login_required(login_url='/login')
def listar_producto(request, id):
    pro = producto.objects.get(id=int(id))
    return render_to_response("carrito/productos_lista.html", {'producto': pro},
                              context_instance=RequestContext(request))

@login_required(login_url='/login')
def carrito_add(request, id):
    if request.method == "POST":
        cant = request.POST['cantidad']
        if int(cant) > 0:
            if not "id_sesion" in request.session:
                request.session["id_sesion"] = hashlib.md5(str(datetime.datetime.now())).hexdigest()
            pro = producto.objects.get(id=int(id))
            carr = Carrito.objects.create(id_sesion=request.session["id_sesion"], estado=False, producto=pro,
                                          cantidad=int(cant))
            contador = request.session['contador']
            request.session['contador'] = contador + 1
    return HttpResponse(request.session['contador'])

@login_required(login_url='/login')
def confirmar_compra(request):
    if request.user.is_authenticated():
        id_sesion = request.session["id_sesion"]
        carr = Carrito.objects.filter(id_sesion=id_sesion)
        return render_to_response("carrito/confirmar_compra.html", {'carr': carr},
                                  context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/usuario/ingresar/")

@login_required(login_url='/login')
def eliminar_de_carrito(request, id):
    if "contador" in request.session:
        contador = request.session['contador']
        request.session['contador'] = contador - 1
        carr = Carrito.objects.get(id=int(id))
        carr.delete()
        return HttpResponseRedirect("/confirmar/compra/")
    else:
        return HttpResponseRedirect("/productos/")

@login_required(login_url='/login')
def realizar_transaccion(request):
    if request.user.is_authenticated():
        usuario = request.user
        u = User.objects.get(username=usuario)
        """Aqui para realizar la transaccion solo lo agregaremos en nuestra tabla pedido"""
        id_sesion = request.session["id_sesion"]
        carr = Carrito.objects.filter(id_sesion=id_sesion)
        """RECORREMOS EL CARRITO EN UN FOR PARA REALIZAR LA TRANSACCION"""
        pre_total = 0
        cantidad = 0
        for i in carr:
            pre_total += float(i.producto.Precio * i.cantidad)
            cantidad += i.cantidad
        trans = Pedido.objects.create(cliente=u, cantidad=cantidad, precio_total=pre_total)
        for i in carr:
            """SELECCIONAMOS EL PRODUCTO PARA REDUCIR EL STOCK"""
            pro = producto.objects.get(id=i.producto.id)
            """NUESTRA CLASE TIENE UNA RELACION DE MUCHOS A MUCHOS ASI QUE LA AGREGAMOS DE ESTA FORMA"""
            trans.producto.add(pro)
            sto = stock.objects.get(reg_pro_id=i.producto.id)
            sto.cantidad = sto.cantidad - i.cantidad
            sto.save()
            pro.save()
        trans.save()
        """Eliminamos el carrito"""
        carr.delete()
        request.session['contador'] = 0
        return HttpResponseRedirect("/factura/" + str(trans.id) + "/")
    else:
        return HttpResponseRedirect("/usuario/ingresar/")

#================= REPORTES================================

def ReporteVentas(request):
    pedido = Pedido.objects.all()
    usuario = perfil_user.objects.all()
    html = render_to_string('reportesPDF/reporteventa.html', {'pagesize': 'A4', 'pedido': pedido, 'usuario': usuario}, context_instance=RequestContext(request))
    return generar_pdf(html)


def generar_pdf(html):
    reporventa = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF:8")), reporventa)
    if not pdf.err:
        return HttpResponse(reporventa.getvalue(), mimetype='application/pdf')
    return HttpResponse("Error en generar el pdf")

@login_required(login_url='/login')
def reporteFiltro(request):
    if request.method == "POST":
        tipo = request.POST["sopcion"]
        if tipo == "1":
            f = request.POST["tfecha"]
            #return HttpResponse(f)
            busqueda=(
                    Q(fecha__icontains=f ))
            pedido = Pedido.objects.filter(busqueda)
            usuario = perfil_user.objects.all()


            html = render_to_string('reportesPDF/reporte_por_fecha.html', {'pagesize': 'A4', 'pedido': pedido, 'usuario':usuario}, context_instance=RequestContext(request))
            return generar_pdf(html)
        if tipo == "2":
            pedido = Pedido.objects.all()
            usuario = perfil_user.objects.all()
            html = render_to_string('reportesPDF/reporte_por_fecha.html', {'pagesize': 'A4', 'pedido': pedido, 'usuario': usuario},context_instance=RequestContext(request))
            return ven_fechas_pdf(html)

    else:
        return HttpResponse("ERROR")

def ven_fechas_pdf(html):
    reporventa = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF:8")), reporventa)
    if not pdf.err:
        return HttpResponse(reporventa.getvalue(), mimetype='application/pdf')
    return HttpResponse("Error en generar el pdf")



def vista_reporte(request):
    return render_to_response('reportesPDF/vista_reporte.html',{},context_instance=RequestContext(request))

#===========FACTURA===========================

def factura(request, id_venta):
    pedido = Pedido.objects.get(id=id_venta)
    usu = perfil_user.objects.get(user=request.user)
    venta = Pedido.objects.filter(id=id_venta)
    #pro=producto.objects.all()
    #for i in venta:
    #   pre= producto.Precio*i.producto.cantidad


    html = render_to_string('reportesPDF/factura.html', {'pagesize': 'A4', 'pedido': pedido, 'usu': usu, 'venta': venta}
        ,context_instance=RequestContext(request))
    return factura_pdf(html)


def factura_pdf(html):
    reporventa = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF:8")), reporventa)
    if not pdf.err:
        return HttpResponse(reporventa.getvalue(), mimetype='application/pdf')
    return HttpResponse("Error en generar el pdf")

#============================= PAYPAL===================================
'''#from paypal.standard.forms import PayPalPaymentsForm
import paypalrestsdk
import logging

def pagocontarjetadecredito(request):
    logging.basicConfig(level=logging.INFO)
    pagar=Pedido.objects.all()
    total=pagar.precio_total
    paypalrestsdk.configure({
        "mode": "sandbox", # sandbox or live
        "client_id": "AcCi2xAa-1BeCPcoGO31cVDwNN4zS_AhXKX5DZ1qMyEaNZmu5prUnLHUPDKB",
        "client_secret": "EC5R1RBQQEcsAkdLiS1BcvMNdh-DaO9QAvHtHQiWUQoJFacukW2m9Nl7q9ms" })
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "credit_card",
            "funding_instruments": [{
                "credit_card": {
                    "type": "visa",
                    "number": "4417119669820331",
                    "expire_month": "11",
                    "expire_year": "2018",
                    "cvv2": "874",
                    "first_name": "Joe",
                    "last_name": "Shopper" }}]},
        "transactions": [{
            "item_list": {
                "items": [{
                "name": "item",
                "sku": "item",
                "price": "1.00",
                "currency": "USD",
                "quantity": 1 }]},

            "amount": {

                "total": total,
                "currency": "USD" },
            "description": "This is the payment transaction description." }]})
    if(payment.create()):
        return render_to_response("ventas/pagorealizado.html",{},RequestContext(request))
    else:
        print payment.error'''
#=======================================================================



#================codigo de facturacion=================================

'''def getBase64(numero):
    diccionario = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
                   "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d",
                   "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x",
                   "y", "z", "+", "/"]
    cociente = 1
    resto = 0
    palabra = ""
    while cociente > 0:
        cociente = numero / 64
        resto = numero % 64
        palabra = diccionario[resto] + palabra
        numero = cociente
    return palabra


def invertir(numero):
    return numero[::-1]


def digito(numero):
    inv = [0, 4, 3, 2, 1, 5, 6, 7, 8, 9]
    mul = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 0, 6, 7, 8, 9, 5], [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
           [3, 4, 0, 1, 2, 8, 9, 5, 6, 7], [4, 0, 1, 2, 3, 9, 5, 6, 7, 8], [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
           [6, 5, 9, 8, 7, 1, 0, 4, 3, 2], [7, 6, 5, 9, 8, 2, 1, 0, 4, 3], [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
           [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]]
    per = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 5, 7, 6, 2, 8, 3, 0, 9, 4], [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
           [8, 9, 1, 6, 0, 4, 3, 5, 2, 7], [9, 4, 5, 3, 1, 2, 6, 8, 7, 0], [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
           [2, 7, 9, 3, 8, 0, 6, 4, 1, 5], [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]]
    num_inv = invertir(numero)
    i = 0
    check = 0
    while i < len(num_inv):
        aux1 = (i + 1) % 8
        aux2 = int(num_inv[i])
        aux3 = per[aux1][aux2]
        check = mul[check][aux3]
        i = i + 1
    return inv[check]


def getModulo(numero):
    return numero % 1073741823


def getRC4(numero,compra):
    estado = []
    codigo = ""
    nrohex = ""
    x, y, index1, index2, nmen, i, op1, aux, op2 = 0, 0, 0, 0, 0, 0, 0, 0, 0
    while i <= 255:
        estado.append(1)
        estado[i] = i
        i = i + 1
    i = 0
    while (i <= 255):
        if compra[index1] == " ":
            op1 = 191
        else:
            op1 = ord(compra[index1])
        index2 = (op1 + estado[i] + index2) % 256
        aux = estado[i]
        estado[i] = estado[index2]
        estado[index2] = aux
        index1 = (index1 + 1) % len(compra)
        i = i + 1
    i = 0
    while (i < len(numero)):
        x = (x + 1) % 256
        y = (estado[x] + y) % 256
        aux = estado[x]
        estado[x] = estado[y]
        estado[y] = aux
        op1 = ord(numero[i])
        op2 = estado[(estado[x] + estado[y]) % 256]
        nmen = op1 ^ op2
        nrohex = hex(nmen).upper()[2:]
        if len(nrohex) == 1:
            nrohex = "0" + nrohex
        codigo = codigo + nrohex + "-"
        i = i + 1
    return codigo[0:len(codigo) - 1]'''
