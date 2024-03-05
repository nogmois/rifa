from django.contrib import admin
from .models import Sorteio, ParticipacaoSorteio, TextbeltApiKey, StripeConfig

@admin.register(Sorteio)
class SorteioAdmin(admin.ModelAdmin):
    list_display = ['nome', 'preco', 'descricao', 'imagem', 'slug', 'numero']  # Adicione 'numero' aqui


class ParticipacaoSorteioAdmin(admin.ModelAdmin):
    list_display = ('nome_participante', 'celular_participante', 'sorteio', 'numeros_selecionados', 'paga')
    search_fields = ['nome_participante', 'sorteio__nome']
    list_filter = ('sorteio',)

# Registro do Modelo no Admin
admin.site.register(ParticipacaoSorteio, ParticipacaoSorteioAdmin)


class TextbeltApiKeyAdmin(admin.ModelAdmin):
    list_display = ('chave', 'descricao')
    search_fields = ('chave', 'descricao')

admin.site.register(TextbeltApiKey)


@admin.register(StripeConfig)
class StripeConfigAdmin(admin.ModelAdmin):
    list_display = ('public_key',)