# Generated by Django 3.0.8 on 2020-08-01 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20200801_1304'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='city',
            field=models.CharField(default='', max_length=30),
        ),
    ]