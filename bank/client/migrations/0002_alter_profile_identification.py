# Generated by Django 4.2.7 on 2023-11-06 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='identification',
            field=models.CharField(max_length=9, unique=True),
        ),
    ]
