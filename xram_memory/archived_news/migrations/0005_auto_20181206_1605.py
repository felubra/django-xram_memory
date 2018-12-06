# Generated by Django 2.1.2 on 2018-12-06 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archived_news', '0004_auto_20181206_1123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archivednews',
            name='status',
            field=models.PositiveIntegerField(choices=[(100, 'Novo'), (200, 'Em fila para processamento'), (300, 'Processado'), (400, 'Publicado'), (401, 'Escondido'), (500, 'Erro no processamento'), (501, 'Erro na captura')], default=100, editable=False, verbose_name='Status'),
        ),
    ]
