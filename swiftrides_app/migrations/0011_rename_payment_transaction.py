# Generated by Django 5.0.3 on 2024-04-27 20:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('swiftrides_app', '0010_payment'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Payment',
            new_name='Transaction',
        ),
    ]
