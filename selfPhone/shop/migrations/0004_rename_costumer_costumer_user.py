# Generated by Django 5.0.4 on 2024-04-18 09:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_rename_picture_smartphone_picture01_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='costumer',
            old_name='costumer',
            new_name='user',
        ),
    ]
