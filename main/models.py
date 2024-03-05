from django.db import models
from django.utils.text import slugify
from django.contrib.postgres.fields import ArrayField

from django.utils import timezone

class Sorteio(models.Model):
    nome = models.CharField(max_length=200)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='imagens_sorteios/')
    slug = models.SlugField(unique=True, blank=True)

    numero = models.IntegerField()

    participacoes = models.ManyToManyField('ParticipacaoSorteio', related_name='sorteios')


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super(Sorteio, self).save(*args, **kwargs)

    def __str__(self):
        return self.nome


class ParticipacaoSorteio(models.Model):
    sorteio = models.ForeignKey(Sorteio, on_delete=models.CASCADE)
    nome_participante = models.CharField(max_length=200)
    celular_participante = models.CharField(max_length=20)
    numeros_selecionados = ArrayField(models.IntegerField())

    data_criacao = models.DateTimeField(default=timezone.now)  # Campo para armazenar a data/hora de criação

    paga = models.BooleanField(default=False)

    def __str__(self):
        return f"Participação de {self.nome_participante} no sorteio {self.sorteio.nome}"


class TextbeltApiKey(models.Model):
    chave = models.CharField(max_length=200)
    descricao = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Textbelt API Key: {self.descricao or self.chave[:10]}..."

        
class StripeConfig(models.Model):
    public_key = models.CharField(max_length=200, verbose_name="Stripe Public Key")
    secret_key = models.CharField(max_length=200, verbose_name="Stripe Secret Key")

    def __str__(self):
        return "Configurações do Stripe"