# Generated by Django 3.1.6 on 2022-02-11 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institucional', '0002_auto_20220210_0947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asignatura',
            name='nombre',
            field=models.CharField(max_length=80, verbose_name='Nombre de Asignatura'),
        ),
    ]
