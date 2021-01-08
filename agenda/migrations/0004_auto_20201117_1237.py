# Generated by Django 3.1.2 on 2020-11-17 17:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0003_auto_20201116_1758'),
    ]

    operations = [
        migrations.AddField(
            model_name='rolelist',
            name='chair',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='chair', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='rolelist',
            name='saa',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='saa', to=settings.AUTH_USER_MODEL),
        ),
    ]