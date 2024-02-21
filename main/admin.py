from django.contrib import admin
from .models import Sorteio

@admin.register(Sorteio)
class SorteioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'descricao', 'slug')
