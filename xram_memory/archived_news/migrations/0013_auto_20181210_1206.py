# Generated by Django 2.1.2 on 2018-12-10 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archived_news', '0012_keyword_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='keyword',
            options={'verbose_name': 'Palavra-chave', 'verbose_name_plural': 'Palavras-chave'},
        ),
        migrations.AlterField(
            model_name='archivednews',
            name='keywords',
            field=models.ManyToManyField(null=True, to='archived_news.Keyword'),
        ),
    ]