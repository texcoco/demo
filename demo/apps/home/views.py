from django.shortcuts import render_to_response
from django.template import RequestContext
from demo.apps.ventas.models import producto
from demo.apps.home.forms import ContactForm, LoginForm
from django.core.mail import EmailMultiAlternatives # Enviamos HTML

from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseRedirect


def index_view(request):
	return render_to_response('home/index.html',context_instance=RequestContext(request))

def about_view(request):
	mensaje = "Esto es un mensaje desde mi vista"
	ctx = {'msg':mensaje}
	return render_to_response('home/about.html',ctx,context_instance=RequestContext(request))

def productos_view(request):
	prod = producto.objects.filter(status=True) # Select * from ventas_productos where status = True
	ctx = {'productos':prod}
	return render_to_response('home/productos.html',ctx,context_instance=RequestContext(request))



def contacto_view(request):
	info_enviado = False # Definir si se envio la informacion o no se envio
	email = ""
	titulo = ""
	texto = ""
	if request.method == "POST":
		formulario = ContactForm(request.POST)
		if formulario.is_valid():
			info_enviado = True
			email = formulario.cleaned_data['Email']
			titulo = formulario.cleaned_data['Titulo']
			texto = formulario.cleaned_data['Texto']

			# Configuracion enviando mensaje via GMAIL
			to_admin = 'alexexc2@gmail.com'
			html_content = "Informacion recibida de [%s] <br><br><br>***Mensaje****<br><br>%s"%(email,texto)
			msg = EmailMultiAlternatives('Correo de Contacto',html_content,'from@server.com',[to_admin])
			msg.attach_alternative(html_content,'text/html') # Definimos el contenido como HTML
			msg.send() # Enviamos  en correo
	else:
		formulario = ContactForm()
	ctx = {'form':formulario,'email':email,'titulo':titulo,'texto':texto,'info_enviado':info_enviado}
	return render_to_response('home/contacto.html',ctx,context_instance=RequestContext(request))


def login_view(request):
	mensaje = ""
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		if request.method == "POST":
			form = LoginForm(request.POST)
			if form.is_valid():
				username = form.cleaned_data['username']
				password = form.cleaned_data['password']
				usuario = authenticate(username=username,password=password)
				if usuario is not None and usuario.is_active:
					login(request,usuario)
					return HttpResponseRedirect('/')
				else:
					mensaje = "usuario y/o password incorrecto"
		form = LoginForm()
		ctx = {'form':form,'mensaje':mensaje}
		return render_to_response('home/login.html',ctx,context_instance=RequestContext(request))

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')
