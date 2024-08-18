from django.shortcuts import render

# Create your views here.

# View for hospital home page
def home(request):
    return render(request,'home.html')