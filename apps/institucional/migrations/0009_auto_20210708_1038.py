# Generated by Django 3.1.6 on 2021-07-08 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('institucional', '0008_auto_20210603_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asignaturausuario',
            name='horario_asignatura',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='institucional.horarioasignatura'),
        ),
    ]