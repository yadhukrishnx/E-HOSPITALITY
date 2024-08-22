from django.contrib import admin
from .models import UserProfile, Appointment, CheckupDetails

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'user_type', 'department', 'phone_no', 'status')
    search_fields = ('user__username', 'name', 'phone_no', 'department')
    list_filter = ('user_type', 'department', 'status')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'appointment_date', 'status', 'created_at', 'payment_status')
    search_fields = ('patient__username', 'doctor__username', 'status')
    list_filter = ('status', 'payment_status', 'appointment_date')

@admin.register(CheckupDetails)
class CheckupDetailsAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'patient', 'checkup_date', 'checkup_status', 'next_visit_date')
    search_fields = ('patient__username', 'appointment__id', 'checkup_status')
    list_filter = ('checkup_status', 'checkup_date', 'next_visit_date')
    readonly_fields = ('checkup_date',)
