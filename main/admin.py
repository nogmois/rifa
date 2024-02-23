from django.contrib import admin
from .models import Sorteio, ParticipacaoSorteio

@admin.register(Sorteio)
class SorteioAdmin(admin.ModelAdmin):
    list_display = ['nome', 'preco', 'descricao', 'imagem', 'slug', 'numero']  # Adicione 'numero' aqui


class ParticipacaoSorteioAdmin(admin.ModelAdmin):
    list_display = ('nome_participante', 'celular_participante', 'sorteio', 'numeros_selecionados', 'paga')
    search_fields = ['nome_participante', 'sorteio__nome']
    list_filter = ('sorteio',)

# Registro do Modelo no Admin
admin.site.register(ParticipacaoSorteio, ParticipacaoSorteioAdmin)