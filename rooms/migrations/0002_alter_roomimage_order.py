# Generated by Django 4.2.15 on 2025-01-06 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomimage',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
