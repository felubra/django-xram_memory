# Generated by Django 2.1.2 on 2018-12-11 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archived_news', '0004_auto_20181211_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archivednews',
            name='force_basic_processing',
            field=models.BooleanField(default=True, help_text='Marque se deseja incluir essa notícia para processamento automático.<br/>Observe que isso sobrescreverá qualquer informação que você tiver inserido manualmente.', verbose_name='Buscar automaticamente informações sobre a notícia'),
        ),
    ]
