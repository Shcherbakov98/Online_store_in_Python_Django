# Generated by Django 3.0.4 on 2020-04-17 15:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200417_1651'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='date_of_birth',
            new_name='date',
        ),
    ]
