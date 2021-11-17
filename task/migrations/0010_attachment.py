# Generated by Django 2.2 on 2019-04-06 16:28

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import task.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("task", "0009_priority_optional"),
    ]

    operations = [
        migrations.CreateModel(
            name="Attachment",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("timestamp", models.DateTimeField(default=datetime.datetime.now)),
                (
                    "file",
                    models.FileField(
                        max_length=255, upload_to=task.models.get_attachment_upload_dir
                    ),
                ),
                (
                    "added_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "task",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="task.Task"),
                ),
            ],
        )
    ]
