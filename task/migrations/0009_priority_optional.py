# Generated by Django 2.1.7 on 2019-03-18 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("task", "0008_mail_tracker")]

    operations = [
        migrations.AlterModelOptions(
            name="task", options={"ordering": ["priority", "created_date"]}
        ),
        migrations.AlterField(
            model_name="task",
            name="priority",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]