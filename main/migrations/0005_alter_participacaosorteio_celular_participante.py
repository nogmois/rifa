# Generated by Django 5.0.2 on 2024-02-22 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_sorteio_numero_participacaosorteio_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participacaosorteio',
            name='celular_participante',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
