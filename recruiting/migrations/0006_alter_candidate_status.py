# Generated by Django 3.2.9 on 2021-11-16 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruiting', '0005_ctc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='status',
            field=models.IntegerField(choices=[(1, 'New'), (2, 'In Process '), (3, 'Selected for interview'), (4, 'Selected after Interviews'), (5, 'Joined'), (6, 'Reject CV'), (7, 'Reject in interview'), (8, 'Rejected Offer')], default=1),
        ),
    ]
