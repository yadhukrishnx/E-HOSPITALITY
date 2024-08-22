from django.contrib import admin
from .models import UserProfile, Appointment, CheckupDetails

# Register UserProfile model with Django admin
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'department', 'phone_no', 'status', 'doctor_availability')
    search_fields = ('user__username', 'name', 'department')
    list_filter = ('user_type', 'department', 'status', 'doctor_availability')

# Register Appointment model with Django admin
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'appointment_date', 'status', 'created_at')
    search_fields = ('patient__username', 'doctor__username', 'appointment_date')
    list_filter = ('status', 'appointment_date')
    ordering = ('-appointment_date',)

# Register CheckupDetails model with Django admin
@admin.register(CheckupDetails)
class CheckupDetailsAdmin(admin.ModelAdmin):
    list_display = ('patient', 'checkup_date', 'next_visit_date', 'checkup_status')
    search_fields = ('patient__username', 'checkup_date')
    list_filter = ('checkup_status', 'checkup_date')

