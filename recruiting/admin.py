from django.contrib import admin
from .models import Candidate, Skill, Interview, CTC
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html


class CTCInline(admin.TabularInline):
    model = CTC
    extra = 0


class InterviewInline(admin.TabularInline):
    model = Interview
    extra = 0


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    pass


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):

    list_display = ('full_name', 'email', 'mobile', 'status', 'view_interview_link',)
    list_editable = ('experience', 'status')
    search_fields = ('email', 'full_name', 'mobile')
    list_filter = ('skills', 'status')

    list_editable = ('status',)

    inlines = [CTCInline]

    def view_interview_link(self, obj):
        count = obj.interviews.count()
        url = (
            reverse("admin:recruiting_interview_changelist")
            + "?"
            + urlencode({"interviews__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} Interview</a>', url, count)

    view_interview_link.short_description = "Interview"


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):

    list_display = ('candidate', 'time', 'status', 'user', 'rating',)
    list_editable = ('status',)
    search_fields = ('candidate', 'remark')
    list_filter = ('status',)
