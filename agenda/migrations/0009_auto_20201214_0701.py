# Generated by Django 3.1.2 on 2020-12-14 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0008_auto_20201202_0805'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='theme',
            field=models.CharField(default=None, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='meeting',
            name='wod',
            field=models.CharField(default=None, max_length=50, null=True),
        ),
    ]
