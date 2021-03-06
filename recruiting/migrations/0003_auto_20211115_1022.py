# Generated by Django 3.2.9 on 2021-11-15 10:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recruiting', '0002_auto_20211115_0830'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='hr',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='candidate', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='refer_by',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='skills',
            field=models.ManyToManyField(blank=True, to='recruiting.Skill'),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='status',
            field=models.IntegerField(choices=[(1, 'New'), (2, 'In Process '), (3, 'Selected for interview'), (4, 'Selected'), (5, 'Joined'), (6, 'Reject CV'), (7, 'Reject in interview'), (8, 'Rejected Offer')], default=1),
        ),
        migrations.CreateModel(
            name='Interview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(verbose_name='Time of Interview')),
                ('status', models.IntegerField(choices=[(2, 'Selected'), (3, 'Rejected '), (1, 'new'), (4, 'Canceled'), (5, "Can't Say")], default=1)),
                ('remark', models.TextField(verbose_name='Put remark here')),
                ('rating', models.IntegerField(verbose_name='Rating out of 10')),
                ('experience', models.IntegerField(verbose_name='Evalution in year exp.')),
                ('candidate', models.ForeignKey(limit_choices_to=models.Q(('status', 3), ('status', 4), _connector='OR'), on_delete=django.db.models.deletion.CASCADE, related_name='interviews', to='recruiting.candidate')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='interviews', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
