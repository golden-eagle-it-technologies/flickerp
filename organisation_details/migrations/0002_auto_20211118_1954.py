# Generated by Django 3.2.9 on 2021-11-18 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisation_details', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='salary_scale',
            field=models.CharField(blank=True, max_length=45, null=True),
        ),
        migrations.DeleteModel(
            name='SalaryScale',
        ),
    ]
