from django.contrib import admin
from core.models import Evento

# Register your models here.

class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data_evento', 'data_criacao') # Aqui é informado os campos que eu quero que apareca
    list_filter = ('usuario',) # Aparece um filtro de nome

admin.site.register(Evento, EventoAdmin) # Acrescentando EventoAdmin para aparecer no admin do django
