from django.urls import path
from .views import (
    UserLoginView, UserLogoutView,
    UserRegisterView, DoctorRegisterView,
    dashboard, approve_leave, reject_leave, patient_dashboard, doctor_dashboard, admin_dashboard, get_doctors, cancel_appointment, add_visit_summary, admin_delete_appointment, admin_edit_appointment
)

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("register/doctor/", DoctorRegisterView.as_view(), name="doctor_register"),

    path("dashboard/", dashboard, name="dashboard"),
    path("dashboard/patient/", patient_dashboard, name="patient_dashboard"),
    path("dashboard/doctor/", doctor_dashboard, name="doctor_dashboard"),
    path("dashboard/admin/", admin_dashboard, name="admin_dashboard"),

    path("get_doctors/", get_doctors, name="get_doctors"),
    path('appointment/<int:appointment_id>/cancel/', cancel_appointment, name='cancel_appointment'),
    path('appointment/<int:appointment_id>/summary/', add_visit_summary, name='add_visit_summary'),
    path('appointments/<int:appointment_id>/edit/', admin_edit_appointment, name='admin_edit_appointment'),
    path('appointments/<int:appointment_id>/delete/', admin_delete_appointment, name='admin_delete_appointment'),
    path("leave/<int:leave_id>/approve/", approve_leave, name="approve_leave"),
    path("leave/<int:leave_id>/reject/", reject_leave, name="reject_leave"),
]

