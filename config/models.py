from django.db import models


class Year(models.Model):
    name = models.CharField("Name of Year", max_length=50)
    start_year = models.DateField()
    end_year = models.DateField()


class Currency(models.Model):
    code = models.CharField(max_length=10, unique=True, default="USD")
    desc = models.CharField(max_length=20, default="US Doler")
    cost = models.CharField(max_length=20, default="1")

    def __str__(self):
        return self.code


class HiringConf(models.Model):
    send_welcome_email = models.BooleanField("Welcome email after Cv added", default=False)
    send_resume_sortlisted_email = models.BooleanField("God fit for Interview, selected Proceess Cv", default=False)
    send_resume_rejected_email = models.BooleanField("Con't Proceess for interview", default=False)
    send_selected_email = models.BooleanField("Selected After Interview", default=False)
    send_rejected_email = models.BooleanField("Rejected after Interview", default=False)
    send_video_interview_email = models.BooleanField("Created Auto interview for video round", default=False)
