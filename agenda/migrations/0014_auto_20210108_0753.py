# Generated by Django 3.1.2 on 2021-01-08 07:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0013_eventlist_item'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Eventlist_item',
            new_name='Eventlist',
        ),
    ]