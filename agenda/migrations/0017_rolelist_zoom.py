# Generated by Django 3.1.2 on 2021-01-17 13:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0016_auto_20210111_0909'),
    ]

    operations = [
        migrations.AddField(
            model_name='rolelist',
            name='zoom',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='zoom', to=settings.AUTH_USER_MODEL),
        ),
    ]