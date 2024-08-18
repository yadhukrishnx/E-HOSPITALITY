from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings

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

# View for Sign in page

def registerpage(request):
    return render(request,'register.html')