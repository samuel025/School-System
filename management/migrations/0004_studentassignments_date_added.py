# Generated by Django 3.1.7 on 2021-05-14 19:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0003_auto_20210514_1908'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentassignments',
            name='date_added',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
