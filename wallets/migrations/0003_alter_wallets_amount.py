# Generated by Django 3.2.18 on 2023-03-24 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallets', '0002_auto_20230324_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallets',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=100),
            preserve_default=False,
        ),
    ]