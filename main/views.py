from django.shortcuts import render, redirect, get_object_or_404
from .forms import SorteioForm, ParticipacaoSorteioForm
from .models import Sorteio, ParticipacaoSorteio
import math
import json

def home(request):
    sorteios = Sorteio.objects.all()
    return render(request, 'index.html', {'sorteios': sorteios})



def sorteio(request):
    sorteios = Sorteio.objects.all()
    return render(request, 'sorteios/sorteios.html', {'sorteios': sorteios})



def detalhe_sorteio(request, slug):
    sorteio = get_object_or_404(Sorteio, slug=slug)
    maior_numero = sorteio.numero
    digitos = int(math.log10(maior_numero)) + 1 if maior_numero else 1
    numeros = list(range(1, maior_numero + 1))

    # Obter todos os números já selecionados para este sorteio
    participacoes = ParticipacaoSorteio.objects.filter(sorteio=sorteio)
    numeros_selecionados = set()
    for participacao in participacoes:
        numeros_selecionados.update(participacao.numeros_selecionados)

    if request.method == 'POST':
        form = ParticipacaoSorteioForm(request.POST)
        if form.is_valid():
            participacao = form.save(commit=False)
            participacao.sorteio = sorteio
            # Transformar os números selecionados de JSON para uma lista de inteiros
            numeros_selecionados_form = json.loads(request.POST.get('numeros_selecionados', '[]'))
            participacao.numeros_selecionados = numeros_selecionados_form
            participacao.save()
            # Redirecionar para uma página de sucesso ou similar
    else:
        form = ParticipacaoSorteioForm()

    return render(request, 'sorteios/detalhe_sorteio.html', {
        'sorteio': sorteio, 
        'numeros': numeros, 
        'digitos': digitos, 
        'form': form,
        'numeros_selecionados': numeros_selecionados
    })

def adm(request):
    if request.method == 'POST':
        form = SorteioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SorteioForm()
    return render(request, 'admin/adm.html', {'form': form})