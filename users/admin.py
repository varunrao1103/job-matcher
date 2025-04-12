from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Job, Application
# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)
    
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'recruiter', 'posted_at')
    search_fields = ('title', 'recruiter__username')
    list_filter = ('posted_at',)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'job_seeker', 'submitted_at', 'match_percentage')
    search_fields = ('job__title', 'job_seeker__username')
    list_filter = ('submitted_at',)