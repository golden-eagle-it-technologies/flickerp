# Generated by Django 3.2.9 on 2021-11-23 21:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0002_auto_20211123_1204'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leave_types',
            name='total_taken',
        ),
        migrations.AlterField(
            model_name='leaveapplication',
            name='leave_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leavs', to='leave.leave_types'),
        ),
    ]
