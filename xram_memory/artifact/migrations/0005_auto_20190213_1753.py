# Generated by Django 2.1.5 on 2019-02-13 19:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('artifact', '0004_auto_20190204_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsimagecapture',
            name='news',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='image_capture', to='artifact.News', verbose_name='Notícia'),
        ),
        migrations.AlterField(
            model_name='newspdfcapture',
            name='news',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pdf_captures', to='artifact.News', verbose_name='Notícia'),
        ),
    ]