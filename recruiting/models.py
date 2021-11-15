from django.db import models
from django.conf import settings
from django.db.models import Q
from field_history.tracker import FieldHistoryTracker


class Skill(models.Model):
    name = models.CharField(max_length=140)

    def __str__(self):
        return self.name


class Candidate(models.Model):
    SOURCE = (
        ('api', 'api'),
        ('website', 'website'),
        ('direct', 'direct'),
        ('email', 'Email'),
        ('refer', "Referal"),
    )

    STATUS = (
        (1, "New"),
        (2, "In Process "),
        (3, "Selected for interview"),
        (4, "Selected"),
        (5, "Joined"),
        (6, "Reject CV"),
        (7, "Reject in interview"),
        (8, "Rejected Offer"),
    )

    full_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, null=True, blank=True)
    mobile = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    cv = models.FileField(upload_to ='uploads/cv/')
    source = models.CharField(max_length=100, choices=SOURCE, default='direct')
    skills = models.ManyToManyField(Skill, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices = STATUS, default=1)
    refer_by = models.CharField(max_length=200, null=True, blank=True)
    experience = models.IntegerField("experience in Year")
    hr = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='candidate', null=True, blank=True)

    field_history = FieldHistoryTracker(['status'])

    def __str__(self):
        return self.full_name


class Interview(models.Model):
    STATUS = (
        (2, "Selected"),
        (3, "Rejected "),
        (1, "new"),
        (4, "Canceled"),
        (5, "Can't Say"),
    )
    candidate = models.ForeignKey(
        Candidate, on_delete=models.CASCADE,
        related_name='interviews', limit_choices_to=Q(status=3) | Q(status=4)
    )
    time = models.DateTimeField("Time of Interview")
    status = models.IntegerField(choices = STATUS, default=1)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True, blank=True,
        related_name='interviews')
    remark = models.TextField("Put remark here", null=True, blank=True)
    rating = models.IntegerField("Rating out of 10", null=True, blank=True)
    experience = models.IntegerField("Evalution in year exp.", null=True, blank=True)

    def __str__(self):
        return self.candidate.full_name
