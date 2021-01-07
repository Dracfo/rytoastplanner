# Generated by Django 3.1.2 on 2020-11-16 22:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0002_meeting_rolelist'),
    ]

    operations = [
        migrations.AddField(
            model_name='rolelist',
            name='ah_counter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ah_counter', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='rolelist',
            name='eval1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='eval1', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='rolelist',
            name='eval2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='eval2', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='rolelist',
            name='eval3',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='eval3', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='rolelist',
            name='geneval',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='geneval', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='rolelist',
            name='quizmaster',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quizmaster', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='rolelist',
            name='speaker1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='speaker1', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='rolelist',
            name='speaker2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='speaker2', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='rolelist',
            name='speaker3',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='speaker3', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='rolelist',
            name='tteval',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tteval', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='rolelist',
            name='ttmaster',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ttmaster', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='rolelist',
            name='facilitator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='facilitator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='rolelist',
            name='timer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='timer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='rolelist',
            name='toastmaster',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='toastmaster', to=settings.AUTH_USER_MODEL),
        ),
    ]
