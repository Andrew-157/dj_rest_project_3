# Generated by Django 4.2.1 on 2023-05-26 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='slug',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
    ]
