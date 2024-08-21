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
    path('bookappointment/<int:doctor_id>/', views.book_appointment_view, name='bookappointment'),
    path('cancel-appointment/<int:appointment_id>/', views.cancel_appointment_view, name='cancel_appointment'),
    path('reschedule-appointment/<int:appointment_id>/', views.reschedule_appointment_view, name='reschedule_appointment'),
    path('discharge/', views.patient_discharge_view, name='discharge'),
    path('tips/', views.patient_tips_view, name='tips'),
    path('nutrition/', views.download_nutrition_guide, name='download_nutrition_guide'),
    path('exercise/', views.download_exercise_plan, name='download_exercise_plan'),
    
    # Admin Related Urls
    path('admin-dashboard/approve/<int:user_id>/', views.approve_user, name='approve_user'),
    path('admin-dashboard/reject/<int:user_id>/', views.reject_user, name='reject_user'),
    
    # Doctor Related Urls
    path('doctor/appointments/', views.doctor_appointments_view, name='doctor_appointments'),
    path('doctor/reschedule-appointment/<int:appointment_id>/', views.doctor_reschedule_appointment_view, name='doctor_reschedule_appointment'),
    path('doctor/appointments/confirm/<int:appointment_id>/', views.confirm_appointment_view, name='confirm_appointment'),
    path('doctor/appointments/reject/<int:appointment_id>/', views.reject_appointment_view, name='reject_appointment'),
]