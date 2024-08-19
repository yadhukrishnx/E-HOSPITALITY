from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegisterForm
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from . models import UserProfile

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
    return render(request,'login.html')



  
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