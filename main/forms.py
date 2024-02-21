from django import forms
from .models import Sorteio, ParticipacaoSorteio

class SorteioForm(forms.ModelForm):
    class Meta:
        model = Sorteio
        fields = ['nome', 'preco', 'descricao', 'numero', 'imagem']


class ParticipacaoSorteioForm(forms.ModelForm):
    class Meta:
        model = ParticipacaoSorteio
        fields = ['nome_participante', 'celular_participante', 'numeros_selecionados']