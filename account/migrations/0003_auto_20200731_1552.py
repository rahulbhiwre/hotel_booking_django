# Generated by Django 3.0.8 on 2020-07-31 15:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_student_name'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Student',
            new_name='Customer',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='is_student',
            new_name='is_customer',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='is_teacher',
            new_name='is_hotel',
        ),
    ]
