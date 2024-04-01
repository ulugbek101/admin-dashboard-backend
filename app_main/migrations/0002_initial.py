# Generated by Django 5.0.3 on 2024-03-30 20:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name="O'qituvchi"),
        ),
        migrations.AddField(
            model_name='group',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name="O'qituvchisi"),
        ),
        migrations.AddField(
            model_name='payment',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_main.group', verbose_name='Guruh'),
        ),
        migrations.AddField(
            model_name='payment',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='pupil',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app_main.group', verbose_name='Guruh'),
        ),
        migrations.AddField(
            model_name='payment',
            name='pupil',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_main.pupil', verbose_name="O'quvchi"),
        ),
        migrations.AddField(
            model_name='group',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app_main.subject', verbose_name='Fan nomi'),
        ),
        migrations.AlterUniqueTogether(
            name='pupil',
            unique_together={('first_name', 'last_name', 'group')},
        ),
    ]
