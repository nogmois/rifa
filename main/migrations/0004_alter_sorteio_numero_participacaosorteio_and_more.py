# Generated by Django 5.0.2 on 2024-02-21 18:45

import django.contrib.postgres.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_sorteio_numero'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sorteio',
            name='numero',
            field=models.IntegerField(),
        ),
        migrations.CreateModel(
            name='ParticipacaoSorteio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_participante', models.CharField(max_length=200)),
                ('celular_participante', models.CharField(max_length=20)),
                ('numeros_selecionados', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('sorteio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.sorteio')),
            ],
        ),
        migrations.AddField(
            model_name='sorteio',
            name='participacoes',
            field=models.ManyToManyField(related_name='sorteios', to='main.participacaosorteio'),
        ),
    ]
