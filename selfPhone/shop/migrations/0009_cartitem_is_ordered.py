# Generated by Django 5.0.4 on 2024-04-22 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_alter_smartphone_manufacturer'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='is_ordered',
            field=models.BooleanField(default=False),
        ),
    ]