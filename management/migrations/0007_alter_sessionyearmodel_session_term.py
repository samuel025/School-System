# Generated by Django 3.2.5 on 2021-07-15 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0006_studentassignments_staff_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sessionyearmodel',
            name='session_term',
            field=models.CharField(choices=[('1st term', '1st term'), ('2nd term', '2nd term'), ('3rd term', '3rd term')], max_length=50),
        ),
    ]
