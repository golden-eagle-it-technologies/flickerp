from django.contrib import admin
from .models import Candidate, Skill, Interview, CTC
from django.utils.safestring import mark_safe


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

    list_display = ('full_name', 'email', 'mobile', 'cv', 'status',)
    list_editable = ('experience', 'status')
    search_fields = ('email', 'full_name', 'mobile')
    list_filter = ('skills', 'status')

    list_editable = ('status',)

    inlines = [CTCInline, InterviewInline]


@admin.register(Interview)
class CandidateAdmin(admin.ModelAdmin):

    list_display = ('candidate', 'time', 'status', 'user', 'rating',)
    list_editable = ('time', 'user')
    search_fields = ('candidate', 'remark')
    list_filter = ('time', 'status')
