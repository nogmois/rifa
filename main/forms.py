from django import forms
from .models import Sorteio, ParticipacaoSorteio

class SorteioForm(forms.ModelForm):
    preco = forms.CharField()  # Campo de texto para aceitar valor formatado

    class Meta:
        model = Sorteio
        fields = ['nome', 'preco', 'numero', 'descricao', 'imagem']


class ParticipacaoSorteioForm(forms.ModelForm):
    class Meta:
        model = ParticipacaoSorteio
        fields = ['nome_participante', 'celular_participante', 'numeros_selecionados']


class TextbeltApiKeyForm(forms.Form):
    chave = forms.CharField(label='Chave da API do Textbelt', max_length=200)