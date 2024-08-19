from django.urls import path
from . import views
from django.contrib.auth import views as auth



urlpatterns = [
    path("",views.home,name="home"),
    path("login/",views.loginpage,name="login"),
    path('logout/', auth.LogoutView.as_view(template_name ='/login.html'), name ='logout'),
    path("register/",views.register,name="register"),
]