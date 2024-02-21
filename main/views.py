from django.shortcuts import render, redirect, get_object_or_404
from .forms import SorteioForm
from .models import Sorteio
import math

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
    return render(request, 'sorteios/detalhe_sorteio.html', {'sorteio': sorteio, 'numeros': numeros, 'digitos': digitos})



def adm(request):
    if request.method == 'POST':
        form = SorteioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SorteioForm()
    return render(request, 'admin/adm.html', {'form': form})