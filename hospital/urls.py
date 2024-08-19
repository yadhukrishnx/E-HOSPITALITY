from django.urls import path
from . import views
from django.contrib.auth import views as auth



urlpatterns = [
    path("",views.home,name="home"),
    path("login/",views.loginpage,name="login"),
    path('logout/', views.customlogout, name ='logout'),
    path("register/",views.register,name="register"),
    
    path('patient-dashboard/', views.patient_dashboard_view, name='patient_dashboard'),
    path('doctor-dashboard/', views.doctor_dashboard_view, name='doctor_dashboard'),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
]