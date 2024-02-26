# Generated by Django 5.0.2 on 2024-02-19 22:00

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_expense'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pupil',
            fields=[
                ('first_name', models.CharField(max_length=200, verbose_name='Ism')),
                ('last_name', models.CharField(max_length=200, verbose_name='Familiya')),
                ('phone_number', models.CharField(max_length=12, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.group', verbose_name='Guruh')),
            ],
            options={
                'unique_together': {('first_name', 'last_name', 'group')},
            },
        ),
    ]