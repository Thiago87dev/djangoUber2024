# Generated by Django 5.0.6 on 2024-07-04 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uber', '0020_resultuber_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultuber',
            name='data_criacao',
            field=models.DateField(),
        ),
    ]