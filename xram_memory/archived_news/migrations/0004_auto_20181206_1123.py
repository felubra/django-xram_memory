# Generated by Django 2.1.2 on 2018-12-06 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archived_news', '0003_auto_20181205_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archivednews',
            name='status',
            field=models.PositiveIntegerField(choices=[(1, 'Novo'), (2, 'Em fila para processamento'), (3, 'Processado'), (4, 'Publicado'), (5, 'Escondido'), (5, 'Erro')], default=1, editable=False, verbose_name='Status'),
        ),
    ]
