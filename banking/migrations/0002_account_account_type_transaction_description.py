# Generated by Django 4.2.15 on 2024-08-12 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='account_type',
            field=models.CharField(default='Savings', max_length=50),
        ),
        migrations.AddField(
            model_name='transaction',
            name='description',
            field=models.CharField(blank=True, max_length=225, null=True),
        ),
    ]
