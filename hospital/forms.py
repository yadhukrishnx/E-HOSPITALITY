from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


USER_TYPE_CHOICES = (
    ('patient', 'Patient'),
    ('doctor', 'Doctor'),
    ('admin', 'Admin'),
)

class UserRegisterForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES)
    email = forms.EmailField()
   
 
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'user_type']
