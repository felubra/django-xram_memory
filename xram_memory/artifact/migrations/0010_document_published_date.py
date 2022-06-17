# Generated by Django 2.1.8 on 2019-05-03 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("artifact", "0009_auto_20190501_1218"),
    ]

    operations = [
        migrations.AddField(
            model_name="document",
            name="published_date",
            field=models.DateTimeField(
                blank=True,
                help_text="Data da publicação original deste documento",
                null=True,
                verbose_name="Data de publicação",
            ),
        ),
    ]
