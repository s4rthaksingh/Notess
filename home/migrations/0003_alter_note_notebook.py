# Generated by Django 5.2.1 on 2025-05-17 18:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_notebook_note_notebook'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='notebook',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.notebook'),
        ),
    ]
