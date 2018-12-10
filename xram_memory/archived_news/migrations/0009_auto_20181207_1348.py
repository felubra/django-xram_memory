# Generated by Django 2.1.2 on 2018-12-07 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archived_news', '0008_auto_20181206_1750'),
    ]

    operations = [
        migrations.AddField(
            model_name='archivednews',
            name='manual_insertion',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='archivednews',
            name='page_pdf_file',
            field=models.FileField(
                blank=True, upload_to='D:\\Felipe\\Projetos\\correntes\\xram-memory\\django-xram_memory\\media\\saved_news_pages\\html', verbose_name='Arquivo da notícia em PDF'),
        ),
        migrations.AlterField(
            model_name='archivednews',
            name='authors',
            field=models.TextField(blank=True, verbose_name='Autores'),
        ),
        migrations.AlterField(
            model_name='archivednews',
            name='images',
            field=models.TextField(blank=True, verbose_name='Imagens'),
        ),
        migrations.AlterField(
            model_name='archivednews',
            name='keywords',
            field=models.TextField(blank=True, verbose_name='palavras-chave'),
        ),
        migrations.AlterField(
            model_name='archivednews',
            name='summary',
            field=models.TextField(
                blank=True, verbose_name='Resumo do artigo'),
        ),
        migrations.AlterField(
            model_name='archivednews',
            name='text',
            field=models.TextField(
                blank=True, verbose_name='Texto da notícia'),
        ),
        migrations.AlterField(
            model_name='archivednews',
            name='top_image',
            field=models.FilePathField(
                blank=True, verbose_name='Imagem principal'),
        ),
    ]