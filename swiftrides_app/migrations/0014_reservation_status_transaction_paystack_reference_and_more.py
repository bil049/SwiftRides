# Generated by Django 5.0.3 on 2024-04-28 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swiftrides_app', '0013_alter_transaction_reference'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='status',
            field=models.CharField(default='pending', max_length=20),
        ),
        migrations.AddField(
            model_name='transaction',
            name='paystack_reference',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='reference',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
