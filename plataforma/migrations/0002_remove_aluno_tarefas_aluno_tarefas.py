# Generated by Django 5.1.5 on 2025-01-26 04:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plataforma', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aluno',
            name='tarefas',
        ),
        migrations.AddField(
            model_name='aluno',
            name='tarefas',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='plataforma.tarefas'),
        ),
    ]
