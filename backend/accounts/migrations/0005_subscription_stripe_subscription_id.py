# Generated by Django 3.1 on 2020-12-19 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20201219_0414'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='stripe_subscription_id',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
