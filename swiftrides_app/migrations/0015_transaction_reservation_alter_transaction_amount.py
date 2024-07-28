# Generated by Django 5.0.3 on 2024-04-29 12:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swiftrides_app', '0014_reservation_status_transaction_paystack_reference_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='reservation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='swiftrides_app.reservation'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.CharField(max_length=30),
        ),
    ]
