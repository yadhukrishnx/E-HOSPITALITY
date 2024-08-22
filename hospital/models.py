from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# User profile model to extend the User model
class UserProfile(models.Model):
    USER_TYPE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('admin', 'Admin'),
    )
    DEPARTMENTS = (
        ('cardiology', 'Cardiology'),
        ('neurology', 'Neurology'),
        ('oncology', 'Oncology'),
        ('orthopedics', 'Orthopedics'),
        ('pediatrics', 'Pediatrics'),
        ('gynaecology', 'Gynaecology'),
        ('general', 'General'),
        ('emergency', 'Emergency'),
    )
    STATUS = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    email = models.EmailField(max_length=50, blank=True, null=True)
    department = models .CharField(max_length=20, choices=DEPARTMENTS, blank=True, null=True)
    phone_no = models.CharField(max_length=20, blank=True, null=True)
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS, default='pending')
    doctor_availability = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username
# Signal to automatically create or update a user profile whenever a User object is created or updated
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.profile.save()
    


class Appointment(models.Model):
    APPOINTMENT_STATUS = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('rescheduled', 'Rescheduled'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )

    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='appointments_as_patient',
        limit_choices_to={'profile__user_type': 'patient'}
    )
    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='appointments_as_doctor',
        limit_choices_to={'profile__user_type': 'doctor'}
    )

    dob = models.DateField(null=True)
    appointment_date = models.DateTimeField(null=True)
    reason_for_visit = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=15, choices=APPOINTMENT_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_status = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Appointment with Dr. {self.doctor.profile.first_name} {self.doctor.profile.last_name} on {self.appointment_date.strftime('%Y-%m-%d %H:%M')}"


class CheckupDetails(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    prescription = models.TextField(null=True)
    observations = models.TextField(null=True)
    next_visit_date = models.DateField(null=True)
    checkup_status = models.BooleanField(null=True, default=False)
    checkup_date = models.DateField(auto_now_add=True)
    

    def __str__(self):
        return f"Checkup for {self.patient.username} on {self.checkup_date}"