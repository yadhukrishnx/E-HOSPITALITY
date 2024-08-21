from django.urls import path
from . import views
from django.contrib.auth import views as auth



urlpatterns = [
    path("",views.home,name="home"),
    path("login/",views.loginpage,name="login"),
    path('logout/', views.customlogout, name ='logout'),
    path("register/",views.register,name="register"),
    path('update-profile/', views.update_profile, name='update_profile'),
    
    path('patient-dashboard/', views.patient_dashboard_view, name='patient_dashboard'),
    path('doctor-dashboard/', views.doctor_dashboard_view, name='doctor_dashboard'),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    
    # Patient Related Urls
    path('appointments/', views.patient_appointments_view, name='appointments'),
    path('discharge/', views.patient_discharge_view, name='discharge'),
    path('tips/', views.patient_tips_view, name='tips'),
    path('nutrition/', views.download_nutrition_guide, name='download_nutrition_guide'),
    path('exercise/', views.download_exercise_plan, name='download_exercise_plan'),
    
    # Admin Related Urls
    path('admin-dashboard/approve/<int:user_id>/', views.approve_user, name='approve_user'),
    path('admin-dashboard/reject/<int:user_id>/', views.reject_user, name='reject_user'),
]