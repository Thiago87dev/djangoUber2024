# Generated by Django 5.0.6 on 2024-06-30 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uber', '0009_remove_resultuber_ganho_hora'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultuber',
            name='horas_trab',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]