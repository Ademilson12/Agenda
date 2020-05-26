from django.shortcuts import render  # redirect # importamos o redirect para utilizar no redirecionamento de paginas
from core.models import Evento # Importando Evento para utilização dos models

# Create your views here.

#def index(request): # Quando não for informado o index, ele vai ser redirecionado para agenda
#    return redirect('/agenda/') 

def lista_eventos(request):
    usuario = request.user
    evento = Evento.objects.filter(usuario=usuario) # Definindo que eu quero trazer apenas o id 1
    dados = {'eventos':evento} # Dicionário
    return render(request, 'agenda.html', dados) # Trazendo o response que foi configurar como um dicionário