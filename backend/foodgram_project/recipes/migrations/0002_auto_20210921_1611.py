# Generated by Django 3.0.5 on 2021-09-21 13:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipeingredient',
            old_name='count',
            new_name='amount',
        ),
    ]
