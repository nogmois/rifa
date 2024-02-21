from django import forms
from .models import Sorteio

class SorteioForm(forms.ModelForm):
    class Meta:
        model = Sorteio
        fields = ['nome', 'preco', 'descricao', 'imagem']
