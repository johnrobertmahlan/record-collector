# Generated by Django 3.1 on 2020-09-02 03:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_listening'),
    ]

    operations = [
        migrations.RenameField(
            model_name='record',
            old_name='release_year',
            new_name='release_date',
        ),
    ]
