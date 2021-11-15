# Generated by Django 3.2.9 on 2021-11-15 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140)),
            ],
        ),
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200)),
                ('email', models.CharField(blank=True, max_length=200, null=True)),
                ('mobile', models.CharField(blank=True, max_length=200, null=True)),
                ('address', models.CharField(blank=True, max_length=500, null=True)),
                ('cv', models.FileField(upload_to='uploads/cv/')),
                ('source', models.CharField(choices=[('api', 'api'), ('website', 'website'), ('direct', 'direct'), ('email', 'Email'), ('refer', 'Referal')], default='direct', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('status', models.IntegerField(choices=[(1, 'New'), (2, 'In Process '), (3, 'interview started'), (4, 'Selected'), (5, 'Joined'), (6, 'Reject CV'), (7, 'Reject in interview'), (8, 'Rejected Offer')], default=1)),
                ('skills', models.ManyToManyField(to='recruiting.Skill')),
            ],
        ),
    ]