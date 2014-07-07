from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

#lo que isimos por el email
from django.core.mail import EmailMultiAlternatives
from venta.apps.usuarios.forms import *
#lo que isismos por el email
from venta.apps.usuarios.models import *
from venta.apps.usuarios.forms import *
from django.contrib.auth.models import User
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required,permission_required
import StringIO
#from xhtml12pdf import pisa
from xhtml2pdf import pisa
from django.template.loader import render_to_string

import json

def verificar(request):
    if request.method=='POST':
        usuario=request.POST['username']
        try:
            u=User.objects.get(username=usuario)
            return HttpResponse("El nombre de usuario ya existe porfavor escoja otro")
        except User.DoesNotExist:
            return HttpResponse("Puede usar el nombre de usuario")
    else:
        return HttpResponse()


def nuevo_usuario(request):
    if request.method == 'POST':
        formulario = UserCreationForm(request.POST)
        formularioPerfil=perfil_userForm(request.POST,request.FILES)
        if formulario.is_valid() and formularioPerfil.is_valid():
            u = formulario.save()
            perfil = formularioPerfil.save()
            perfil.user=u

            perfil.per_user=perfil
            perfil.save()
        else:
            return HttpResponseRedirect('/usuario/new/')
        return HttpResponseRedirect('/login/')
    else:
        formulario = UserCreationForm()
        formularioPerfil=perfil_userForm()
    return render_to_response('new_user.html',{'formulario':formulario,'formularioPerfil':formularioPerfil}, context_instance=RequestContext(request))


def login_view(request):
    mensaje = ""
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        if request.method == "POST":
            form =LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['passsword']

                usuario = authenticate(username=username,password=password)
                if usuario is not None and usuario.is_active:
                    login(request,usuario)
                    return HttpResponseRedirect('/')
                else:
                    mensaje = "usuario y/o password incorrecto"
        form = LoginForm()
        ctx ={'form':form,'mensaje':mensaje}
        return render_to_response('login.html',ctx,context_instance=RequestContext(request))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def contacto(request):
    info_enviado = False
    email = ""
    titulo = ""
    texto = ""
    if request.method == "POST":
        formulario = ContactoForm(request.POST)
        if formulario.is_valid():
            info_enviado = True
            email = formulario.cleaned_data['Email']
            titulo = formulario.cleaned_data['Titulo']
            texto = formulario.cleaned_data['Texto']
            to_admin = 'ocamporoberto97@gmail.com'
            html_content = "Informacion recibida de [%s]<br><br><br>***Mensaje***<br><br>%s" % (email, texto)
            msg = EmailMultiAlternatives('Correo de Contacto', html_content, 'from@server.com', [to_admin])
            msg.attach_alternative(html_content, 'text/html')
            msg.send()

    else:
        formulario = ContactoForm()
    ctx = {'form': formulario, "email": email, "titulo": titulo, "texto": texto, "info_enviado": info_enviado}
    return render_to_response('contactoform.html', ctx, context_instance=RequestContext(request))

@login_required(login_url='/login')
def update_usuario(request,id):
    if request.user.is_authenticated():
        usuario=User.objects.get(id=id)
        usu=perfil_user.objects.get(user_id=id)
        if request.method=='POST':
            formulario=fusuario(request.POST)
            if formulario.is_valid():
                contrasena=request.POST["password"]
                usuario.set_password(contrasena)
                usuario.save()

                return HttpResponseRedirect('/')
        else:

            formulario=fusuario()
        return render_to_response("actualizar_usuario.html",{"usuario":formulario},context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')




def re_usuario(request):
    usu=perfil_user.objects.all()
    html=render_to_string('reportesPDF/reporteusuario.html',{'pagesize':'A4','usu':usu},context_instance=RequestContext(request))
    return generar_pdf(html)

def generar_pdf(html):
    resultado=StringIO.StringIO()
    pdf=pisa.pisaDocument(StringIO.StringIO(html.encode("UTF:8")),resultado)
    if not pdf.err:
        return HttpResponse(resultado.getvalue(),mimetype='application/pdf')
    return HttpResponse("Error en generar el pdf")

#def update_usuario(request,id):
#    perfil=perfil_user.objects.get(id=id)
#    form=perfil_userForm(perfil)
#    if request.method=="POST":
#        form=perfil_userForm(request.POST)
#        if form.is_valid():
#            nombre=request.POST["nombre"]
#            ap_paterno=request.POST["ap_paterno"]
#            ap_materno=request.POST["ap_materno"]
#            CI_NIT=request.POST["CI_NIT"]
#            email=request.POST["email"]
#            idPerfil=id
#            perfil=perfil_user.objects.get(id=idPerfil)
#            perfil.nombre=nombre
#            perfil.ap_paterno=ap_paterno
#            perfil.ap_materno=ap_materno
#            perfil.CI_NIT=CI_NIT
#            perfil.email=email
#            perfil.save()
#            respuesta={"exito":True}
#            return HttpResponse(json.dumps(respuesta),content_type="application/json")
#    return render_to_response("actualizar_usuario.html",{"usuario":form},RequestContext(request))
