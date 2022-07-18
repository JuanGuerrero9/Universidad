# Generated by Django 3.1.6 on 2022-02-23 21:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('institucional', '0003_auto_20220211_0138'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asignaturaantecesora',
            name='antecesora',
        ),
        migrations.RemoveField(
            model_name='asignaturaantecesora',
            name='asignatura',
        ),
        migrations.AddField(
            model_name='asignatura',
            name='antecesora',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='institucional.asignatura'),
        ),
        migrations.DeleteModel(
            name='Antecesora',
        ),
        migrations.DeleteModel(
            name='AsignaturaAntecesora',
        ),
    ]