# Generated by Django 3.2.9 on 2021-11-17 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organisation_details', '0001_initial'),
        ('employees', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobAdvertisement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('education', models.CharField(max_length=20)),
                ('vacancy', models.IntegerField()),
                ('experience', models.IntegerField()),
                ('post_date', models.DateField(auto_now=True)),
                ('description', models.TextField()),
                ('show_salary', models.BooleanField(default=True)),
                ('deadline', models.DateField()),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='title', to='organisation_details.position')),
            ],
        ),
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cv', models.FileField(upload_to='cvs/')),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_application', to='employees.employee')),
                ('job_ad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recruitment.jobadvertisement')),
            ],
        ),
    ]