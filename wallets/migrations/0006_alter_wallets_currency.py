# Generated by Django 3.2.18 on 2023-03-28 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallets', '0005_alter_wallets_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallets',
            name='currency',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]