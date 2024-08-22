from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegisterForm
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from . models import UserProfile,Appointment,CheckupDetails
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.utils import timezone

# Create your views here.

# View for hospital home page
def home(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        send_mail(
            name,
            message,
            email,
            [settings.EMAIL_HOST_USER],
        )
        return render(request, 'home.html', {'success_message': 'Your message has been sent successfully!'})
    return render(request,'home.html')

# View for login page

def loginpage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            user_profile = user.profile
            if user_profile.status == 'pending':
                messages.error(request, 'Your account is not approved yet. Please wait for approval.')
                logout(request)
                return redirect('login')
            elif user_profile.status == 'cancelled':
                messages.error(request, 'Your account has been cancelled. Please contact the admin.')
                logout(request)
                return redirect('login')
            elif user_profile.status == 'confirmed':
                if user_profile.user_type == 'patient':
                    return redirect('patient_dashboard')
                elif user_profile.user_type == 'doctor':
                    return redirect('doctor_dashboard')
                elif user_profile.user_type == 'admin':
                    return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request,'login.html')

def customlogout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')
  
########### register here ##################################### 
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_profile = UserProfile.objects.get(user=user)
            user_profile.username = form.cleaned_data.get('username')
            user_profile.email = form.cleaned_data.get('email')
            user_profile.user_type = form.cleaned_data.get('user_type')
            if user_profile.user_type == 'doctor':
                user_profile.department = form.cleaned_data.get('department')
                
            user_profile.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            
            ######################### mail system #################################### 
            htmly = get_template('Email.html')
            d = { 'username': username }
            subject, from_email, to = 'Welcome to Nuclear Hospital HMS', 'yadhukrishnx.dev@gmail.com', email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
            ################################################################## 
            messages.success(request, f'Your account has been created ! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def update_profile(request):
    if request.method == 'POST':
        user_profile = get_object_or_404(UserProfile, user=request.user)
        user_profile.name = request.POST.get('full_name')
        user_profile.age = request.POST.get('age')
        user_profile.address = request.POST.get('address')
        user_profile.phone_no = request.POST.get('phone_number')
        user_profile.save()
        if request.user.profile.user_type == 'patient':
            return redirect('patient_dashboard')
        else:
            return redirect('doctor_dashboard')
    return render(request, 'updateprofile.html')

 #########################Dashboard views######################################### 
@login_required
def patient_dashboard_view(request):
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)
    
    appointment = Appointment.objects.all().filter(patient=user)
    if appointment.exists():
        appointment = appointment.first()
    else:
        appointment = None

    doctors = UserProfile.objects.filter(user_type='doctor')
    
    dict = {
        'doctor_name': appointment.doctor.profile.name if appointment else '',
        'department': appointment.doctor.profile.department if appointment else '',
        'patient_name': appointment.patient.profile.name if appointment else '',
        'patient_dob': appointment.dob if appointment else '',
        'patient_phone': appointment.patient.profile.phone_no if appointment else '',
        'patient_age': appointment.patient.profile.age if appointment else '',
        'appointment_status' : appointment.status if appointment else '',
        'appointment_id': appointment.id if appointment else '',
        'created_on': appointment.created_at if appointment else '',
        'appointment_date': appointment.appointment_date if appointment else '',
        'current_year': timezone.now().year,
        'appointment': appointment if appointment else '',
        'user_profile': user_profile ,
        'doctors':doctors
    }
    
    if user_profile.name == None or user_profile.name == '' or user_profile.address == None :
        return redirect('update_profile')
    
    return render(request, 'patient/dashboard.html',dict)


@login_required
def doctor_dashboard_view(request):
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)
    # Check if user profile is complete
    if user_profile.name == None or user_profile.name == '' or user_profile.address == None :
        return redirect('update_profile')
    # Calculate today's date
    today = timezone.now().date()
    
    # Count today's appointments
    today_appointments_count = Appointment.objects.filter(
        doctor=user,
        appointment_date__date=today
    ).count()

    # Count pending appointments
    pending_appointments_count = Appointment.objects.filter(
        doctor=user,
        status='pending'
    ).count()

    context = {
        'user_profile': user_profile,
        'today_appointments_count': today_appointments_count,
        'pending_appointments_count': pending_appointments_count,
    }

    return render(request, 'doctor/dashboard.html', context)
@login_required
def admin_dashboard_view(request):
    
    pendingusers = UserProfile.objects.filter(status='pending')
    patients = UserProfile.objects.filter(user_type='patient')
    doctors = UserProfile.objects.filter(user_type='doctor')
    admins = UserProfile.objects.filter(user_type='admin')
    return render(request, 'admin/dashboard.html' ,{
      
        'pendingusers': pendingusers,
        'patients': patients,
        'doctors': doctors,
        'admins': admins,
    })


 #########################Patient views######################################### 
 
@login_required
def patient_appointments_view(request):
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)
    appointments = Appointment.objects.filter(patient=user)
    
    context = {
        'appointments':appointments,
        'user_profile': user_profile
    }
    return render(request, 'patient/appointments.html',context)
@login_required
def book_appointment_view(request, doctor_id):
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)
    doctor_profile = get_object_or_404(UserProfile, pk=doctor_id)
    doctor = doctor_profile.user

    if request.method == 'POST':
        # Create the appointment
        appointment = Appointment(
            patient=user,
            doctor=doctor,
            dob=request.POST.get('dob'),
            reason_for_visit=request.POST.get('reason'),
            appointment_date=request.POST.get('appointment_date'),
            status='pending'  # Set default status to 'pending'
        )
        appointment.save()

        # Create CheckupDetails, ensuring all required fields are set
        CheckupDetails.objects.create(
            appointment=appointment,
            patient=user,  # Ensure patient is set
            prescription='',  # Assuming default values for optional fields
            observations='',
            next_visit_date=None,
            checkup_status=False
        )

        messages.success(request, "Appointment has been successfully booked. Wait for approval from the doctor.")
        return redirect('appointments')

    return render(request, 'patient/bookappointment.html', {'doctor': doctor, 'user_profile': user_profile})

@login_required
def cancel_appointment_view(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)
    if appointment.status == 'pending':
        appointment.status = 'cancelled'
        appointment.save()
        messages.success(request, "Appointment has been cancelled.")
    else:
        messages.error(request, "You can only cancel pending appointments.")
    return redirect('appointments')


@login_required
def reschedule_appointment_view(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)
    if request.method == 'POST':
        # Validate and update the appointment with new date/time
        new_date = request.POST.get('appointment_date')
        if new_date:
            appointment.appointment_date = new_date
            appointment.status = 'pending'  # Reset status to pending after rescheduling
            appointment.save()
            messages.success(request, "Appointment has been rescheduled.")
            return redirect('appointments')
        else:
            messages.error(request, "Please provide a valid appointment date.")
    return render(request, 'patient/reschedule_appointment.html', {'appointment': appointment})

@login_required
def patient_discharge_view(request):
    return render(request, 'patient/discharge.html')

@login_required
def patient_tips_view(request):
    return render(request, 'patient/tips.html')


########################## Patient Downloads #########################################

import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse

@login_required
def download_nutrition_guide(request):
    dict={
        'name':request.user.username
        
    }
    return render_to_pdf('patient/nutritionguide.html',dict)
def download_exercise_plan(request):
    dict={
        'name':request.user.username
    }
    return render_to_pdf('patient/exerciseplan.html',dict)

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return
    
    
    
############################ Admin view #############################################
@login_required
@require_POST
def approve_user(request, user_id):
    user_profile = get_object_or_404(UserProfile, user_id=user_id)
    user_profile.status = 'confirmed'
    user_profile.save()
    return redirect('admin_dashboard')

@login_required
@require_POST
def reject_user(request, user_id):
    user_profile = get_object_or_404(UserProfile, user_id=user_id)
    user_profile.status = 'cancelled'
    user_profile.save()
    return redirect('admin_dashboard')

@login_required
def doctor_appointments_view(request):
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)
    checkup = CheckupDetails.objects.all()
    appointments = Appointment.objects.filter(doctor=user)
    return render(request, 'doctor/doctor_appointments.html', {'appointments': appointments, 'checkup':checkup, 'user_profile': user_profile})

@login_required
def confirm_appointment_view(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user)
    if appointment.status == 'pending':
        appointment.status = 'confirmed'
        appointment.save()
        messages.success(request, "Appointment confirmed.")
        # Optionally, send a notification or email to the patient
    return redirect('doctor_appointments')

@login_required
def reject_appointment_view(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user)

    appointment.status = 'cancelled'
    appointment.save()
    messages.success(request, "Appointment rejected.")
        
    return redirect('doctor_appointments')

@login_required
def doctor_reschedule_appointment_view(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        # Validate and update the appointment with new date/time
        new_date = request.POST.get('appointment_date')
        if new_date:
            appointment.appointment_date = new_date
            appointment.status = 'pending'  # Reset status to pending after rescheduling
            appointment.save()
            messages.success(request, "Appointment has been rescheduled.")
            return redirect('doctor_appointments')
        else:
            messages.error(request, "Please provide a valid appointment date.")
    return render(request, 'doctor/reschedule_appointment.html', {'appointment': appointment})

@login_required
def doctor_availability_view(request):
    user = request.user
    user_profile = user.profile
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        profile.doctor_availability = not profile.doctor_availability
        profile.save()
        return redirect('doctor_availability')
    return render(request, 'doctor/availability.html',{'profile': profile , 'user_profile':user_profile})

@login_required
def doctor_checkup(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    checkup, created = CheckupDetails.objects.get_or_create(
        appointment=appointment,
        defaults={'patient': appointment.patient}
    )


    if request.method == 'POST':
        checkup.prescription = request.POST.get('prescription')
        checkup.next_visit_date = request.POST.get('next_visit_date')
        checkup.observations = request.POST.get('observations')
        checkup.checkup_status = True
        checkup.save()
        appointment.status = 'completed'
        appointment.save()
        return redirect('doctor_appointments')
        
    return render(request, 'doctor/checkup.html', {'appointment': appointment, 'checkup': checkup})



@login_required
def checkup_report(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    checkup = get_object_or_404(CheckupDetails, patient=appointment.patient, checkup_date=appointment.appointment_date)
    appointment.status = 'confirmed'
    context = {
        'doctor_name': appointment.doctor.profile.name,
        'department': appointment.doctor.profile.department,
        'patient_name': appointment.patient.profile.name,
        'patient_dob': appointment.dob,
        'patient_phone': appointment.patient.profile.phone_no,
        'patient_age': appointment.patient.profile.age,
        'checkup_date': checkup.checkup_date,
        'observations': checkup.observations,
        'prescription': checkup.prescription,
        'next_visit_date': checkup.next_visit_date,
        'current_year': timezone.now().year,
        'appointment': appointment
    }
    return render(request, 'checkup_report.html', context,)

@login_required
def download_checkup_report(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    checkup = get_object_or_404(CheckupDetails, appointment=appointment)
    if appointment.payment_status:
        return redirect('make_payment', appointment_id)
    
    dict = {    
        'doctor_name': appointment.doctor.profile.name,
        'department': appointment.doctor.profile.department,
        'patient_name': appointment.patient.profile.name,
        'patient_dob': appointment.dob,
        'patient_phone': appointment.patient.profile.phone_no,
        'patient_age': appointment.patient.profile.age,
        'checkup_date': checkup.checkup_date,
        'observations': checkup.observations,
        'prescription': checkup.prescription,
        'next_visit_date': checkup.next_visit_date,
        'current_year': timezone.now().year,
        'appointment': appointment,
    }
    return render_to_pdf('checkup_report.html',dict)


# Stripe payment gateway

import stripe
from django.urls import reverse


def make_payment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    
    if request.method == 'POST':
        appointment.payment_status = True
        # Create the line item for the report with a fixed price of ₹200
        line_item = {
            'price_data': {
                'currency': 'INR',
                'unit_amount': 20000,  # ₹200 = 20000 paise
                'product_data': {
                    'name': 'Report Download',
                },
            },
            'quantity': 1,
        }

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[line_item],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('checkup_report', args=[appointment_id ])),
            cancel_url=request.build_absolute_uri(reverse('appointments')) + '?message=' + 'Payment+failed!',
        )

        return redirect(checkout_session.url, code=303)
    if appointment.payment_status == True:
        return redirect('download_checkup_report', appointment_id)
    else:
        return render(request, 'patient/make_payment.html', {'appointment': appointment})
    
   