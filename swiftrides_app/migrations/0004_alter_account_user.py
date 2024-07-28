# Generated by Django 5.0.3 on 2024-04-02 21:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swiftrides_app', '0003_alter_account_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
