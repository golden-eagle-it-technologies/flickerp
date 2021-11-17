# Generated by Django 3.2.9 on 2021-11-17 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruiting', '0006_alter_candidate_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='interview',
            options={'permissions': (('can_list_all_records', 'User can see all interviews'),)},
        ),
        migrations.AlterField(
            model_name='candidate',
            name='experience',
            field=models.FloatField(verbose_name='experience in Year'),
        ),
        migrations.AlterField(
            model_name='ctc',
            name='current',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='ctc',
            name='expected',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='ctc',
            name='offered',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='interview',
            name='experience',
            field=models.FloatField(blank=True, null=True, verbose_name='Evalution in year exp.'),
        ),
        migrations.AlterField(
            model_name='interview',
            name='rating',
            field=models.FloatField(blank=True, null=True, verbose_name='Rating out of 10'),
        ),
    ]
