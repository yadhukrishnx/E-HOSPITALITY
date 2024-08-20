from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegisterForm
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from . models import UserProfile
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

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
            
            user_profile.email = form.cleaned_data.get('email')
            user_profile.user_type = form.cleaned_data.get('user_type')
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


 #########################Dashboard views######################################### 
@login_required
def patient_dashboard_view(request):
    return render(request, 'patient/dashboard.html')

@login_required
def doctor_dashboard_view(request):
    return render(request, 'doctor/dashboard.html')

@login_required
def admin_dashboard_view(request):
    return render(request, 'admin/dashboard.html')


 #########################Patient views######################################### 
 
@login_required
def patient_appointments_view(request):
    return render(request, 'patient/appointments.html')

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
    