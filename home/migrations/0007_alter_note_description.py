# Generated by Django 5.2.1 on 2025-05-18 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_alter_activity_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='description',
            field=models.CharField(max_length=5000),
        ),
    ]
