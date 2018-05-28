from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms_sim import SimulacionForm, TerrenoForm, HumedadForm
from .multiforms import MultipleFormsView
from .models import *
from .utilidades import *

# Create your views here.

def inicio(request):
	hay_busqueda=False
	simulaciones=list()
	haySimu=Simulacion.objects.filter().exists()
	if haySimu:
		sims=Simulacion.objects.filter(compartir=True)
		nomFer=list()
		sList=list()
		for sim in sims:
			applies=Aplicacion.objects.filter(simulacion=sim)
			for ap in applies:
				nomFer.append(ap.fertilizante)
			sList.append(sim)
			sList.append(nomFer)
			simulaciones.append(sList)
			sList=[] #vaciando lista
			nomFer=[] #vaciando los nombre de los fertilizantes	

	if request.method=='POST':
		if 'f_buscar' in request.POST:
			busqueda=request.POST.get('buscar')
			search=busqueda.lower()
			simulaciones=buscar(simulaciones,search)
			if simulaciones:
				hay_busqueda='Resultados de la busqueda: '+busqueda
			else:
				hay_busqueda='No se encontro nunguna coincidencia de: '+busqueda
	if haySimu:
		haySimu=False
	else:
		haySimu='No hay ninguna simulacion que haya sido compartidas por los usuarios'
	contexto = {
		'simu':haySimu,
		'busqueda':hay_busqueda,
		'simulaciones':simulaciones,
	}
	return render(request, "main/index.html", contexto)

def ayuda(request):
	return render(request,'ayuda.html',{})


@login_required()
def direccionar(request):
	if request.user.is_authenticated:
		return redirect('mi_espacio', username=request.user.username)
	else:
		return redirect('inicio') 

		
@login_required()
def mi_espacio(request, username,op='all'):
	if username == request.user.username:
		hay_busqueda=False
		if op=='all' or op=='shared' or op=='private':
			simulaciones=list()
			if op=='all':
				activo=['active','','']
				haySimu=Simulacion.objects.filter(usuario=request.user).exists()
				if haySimu:
					sims=Simulacion.objects.filter(usuario=request.user)
					nomFer=list()
					sList=list()
					for sim in sims:
						applies=Aplicacion.objects.filter(simulacion=sim)
						for ap in applies:
							nomFer.append(ap.fertilizante)
						sList.append(sim)
						sList.append(nomFer)
						simulaciones.append(sList)
						sList=[] #vaciando lista
						nomFer=[] #vaciando los nombre de los fertilizantes
				if request.method=='POST':
					if 'f_buscar' in request.POST:
						busqueda=request.POST.get('buscar')
						search=busqueda.lower()
						simulaciones=buscar(simulaciones,search)
						hay_busqueda=True
					if 'f_delete' in request.POST:
						id_sim=request.POST.get('id_sim')
						simulacion=Simulacion.objects.get(id=id_sim)
						simulacion.delete()
						return redirect('mi_espacio',username=request.user.username)

			elif op=='shared':
				activo=['','active','']
				haySimu=Simulacion.objects.filter(compartir=True).exists()
				if haySimu:
					sims=Simulacion.objects.filter(compartir=True)
					nomFer=list()
					sList=list()
					for sim in sims:
						applies=Aplicacion.objects.filter(simulacion=sim)
						for ap in applies:
							nomFer.append(ap.fertilizante)
						sList.append(sim)
						sList.append(nomFer)
						simulaciones.append(sList)
						sList=[] #vaciando lista
						nomFer=[] #vaciando los nombre de los fertilizantes
				if request.method=='POST':
					if 'f_buscar' in request.POST:
						busqueda=request.POST.get('buscar')
						search=busqueda.lower()
						simulaciones=buscar(simulaciones,search)
						hay_busqueda=True
					if 'f_delete' in request.POST:
						id_sim=request.POST.get('id_sim')
						simulacion=Simulacion.objects.get(id=id_sim)
						simulacion.delete()
						return redirect('mi_espacio_op',username=request.user.username, op='shared')	
			else:
				activo=['','','active']
				haySimu=Simulacion.objects.filter(compartir=False).exists()
				if haySimu:
					sims=Simulacion.objects.filter(compartir=False)
					nomFer=list()
					sList=list()
					for sim in sims:
						applies=Aplicacion.objects.filter(simulacion=sim)
						for ap in applies:
							nomFer.append(ap.fertilizante)
						sList.append(sim)
						sList.append(nomFer)
						simulaciones.append(sList)
						sList=[] #vaciando lista
						nomFer=[] #vaciando los nombre de los fertilizantes
				if request.method=='POST':
					if 'f_buscar' in request.POST:
						busqueda=request.POST.get('buscar')
						search=busqueda.lower()
						simulaciones=buscar(simulaciones,search)
						hay_busqueda=True
					if 'f_delete' in request.POST:
						id_sim=request.POST.get('id_sim')
						simulacion=Simulacion.objects.get(id=id_sim)
						simulacion.delete()
						return redirect('mi_espacio_op',username=request.user.username, op='private')

		else:
			return redirect('mi_espacio_op', username=request.user.username, op='all')

		if hay_busqueda:
			if simulaciones:
				hay_busqueda='Resultados de la busqueda: '+busqueda
			else:
				hay_busqueda='No se encontro nunguna coincidencia de: '+busqueda
		if haySimu:
			haySimu=False
		else:
			haySimu='No se encontraron simulaciones'

		contexto = {
			'nombre': request.user.first_name+' '+request.user.last_name,
			'simu':haySimu,
			'simulaciones':simulaciones,
			'busqueda':hay_busqueda,
			'activo':activo,
		}
		return render(request, "main/mi_espacio.html", contexto)
	else:
		return redirect('mi_espacio_op', username=request.user.username)


class MultipleFormsDemoView(MultipleFormsView):
    template_name = "main/SimulacionForm.html"
    success_url = reverse_lazy("sim_lista")
    forms_classes = [
        SimulacionForm,
        TerrenoForm,
        HumedadForm,
    ]

    def get_forms_classes(self):
        ##forms_classes = super(MultipleFormsDemoView, self).get_forms_classes()
        return super(MultipleFormsDemoView, self).get_forms_classes()

    def form_valid(self, form):
        print("yay it's valid!")
        return super(MultipleFormsDemoView).form_valid(form)




# def config(request):

# 	if request.method == 'POST':
# 		hayConfig=Configuracion.objects.filter(usuario=request.user).exists() #verificando que exista
# 		if hayConfig: #si ya hay config solo modificar
# 			config=Configuracion.objects.filter(usuario=request.user) #extraer solo la config del user
# 			form=ConfigForm(request.POST,instance=config)
# 			if form.is_valid():
# 				config= form.save()
# 				config.save()
# 		else: #si no hay config crearla
# 			form = ConfigForm(request.POST)
# 			if form.is_valid():
# 				config= form.save()
# 				config.save()
# 	else:
# 		form = ConfigForm()


# 	if request.method=='POST': #solo se metera cuando envien un formulario
# 		hayConfig=Configuracion.objects.filter(usuario=request.user).exists() #verificando que exista
# 		precio=request.POST.get('input_precio_maiz') #obtener el valor que ingreso el user en el form
# 		if hayConfig: #si ya hay config solo modificar
# 			config=Configuracion.objects.filter(usuario=request.user) #extraer solo la config del user
# 			config.precio_maiz=precio #setiar el valor que metio el user
# 			config.save()  #guardar todo los cambios
# 		else: #si no hay config crearla
# 			config=Configuracion(usuario=request.user, precio_maiz=precio)#creando una nueva config
# 			config.save() #guardando los cambios




		