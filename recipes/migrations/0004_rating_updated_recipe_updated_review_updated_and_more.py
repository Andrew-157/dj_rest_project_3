# Generated by Django 4.2.3 on 2023-07-29 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_alter_review_options_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='review',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='rating',
            name='published',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]