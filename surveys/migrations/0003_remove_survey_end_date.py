# Generated by Django 5.1.3 on 2024-12-22 03:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0002_alter_survey_end_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='survey',
            name='end_date',
        ),
    ]