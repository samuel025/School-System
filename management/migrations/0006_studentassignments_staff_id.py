# Generated by Django 3.1.7 on 2021-05-15 09:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0005_studentassignments_course_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentassignments',
            name='staff_id',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='management.staffs'),
            preserve_default=False,
        ),
    ]
