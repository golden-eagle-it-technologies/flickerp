# Generated by Django 3.2.9 on 2021-11-17 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contracts', '0001_initial'),
        ('employees', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='termination',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employees.employee'),
        ),
        migrations.AddField(
            model_name='offence',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employees.employee'),
        ),
        migrations.AddField(
            model_name='offence',
            name='penalty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contracts.penalty'),
        ),
        migrations.AddField(
            model_name='contract',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employees.employee'),
        ),
    ]