# Generated by Django 4.1.9 on 2023-06-16 08:00

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_question_wrong_answers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='wrong_answers',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), default=list, size=None),
        ),
    ]
