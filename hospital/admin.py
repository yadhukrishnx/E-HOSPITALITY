from django.contrib import admin

# Register your models here.

# admin.py

from django.contrib import admin
from .models import UserProfile, Appointment

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_no', 'first_name', 'last_name', 'user_type')
    search_fields = ('user__username', 'phone_no', 'first_name', 'last_name', 'user_type')
    list_filter = ('user_type',)

admin.site.register(UserProfile, UserProfileAdmin)


class AppointmentAdmin(admin.ModelAdmin):
    # Define the fields to display in the list view
    list_display = ('patient', 'doctor', 'appointment_date', 'status', 'created_at')
    
    # Define filters for the list view
    list_filter = ('status', 'doctor', 'appointment_date')
    
    # Add search functionality to the admin interface
    search_fields = ('patient__username', 'doctor__username', 'reason_for_visit')
    
    # Define the fields to be displayed in the detail view
    fields = ('patient', 'doctor', 'dob', 'appointment_date', 'reason_for_visit', 'status')
    

    # Optionally, define which fields should be read-only
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Appointment, AppointmentAdmin)