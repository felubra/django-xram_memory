# Generated by Django 2.1.5 on 2019-02-17 21:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('artifact', '0007_auto_20190217_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='newspaper',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='news', to='artifact.Newspaper'),
        ),
    ]