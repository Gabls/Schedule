# Generated by Django 4.2.5 on 2023-09-28 04:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_event_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='fullDate',
            new_name='full_date',
        ),
    ]
