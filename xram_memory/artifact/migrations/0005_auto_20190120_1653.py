# Generated by Django 2.1.2 on 2019-01-20 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artifact', '0004_auto_20190120_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='file_hash',
            field=models.CharField(blank=True, editable=False, help_text='Hash único do arquivo em MD5', max_length=32),
        ),
    ]