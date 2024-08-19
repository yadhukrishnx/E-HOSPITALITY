from django.contrib import admin

# Register your models here.

# admin.py

from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_no', 'first_name', 'last_name', 'user_type')
    search_fields = ('user__username', 'phone_no', 'first_name', 'last_name', 'user_type')
    list_filter = ('user_type',)

admin.site.register(UserProfile, UserProfileAdmin)
