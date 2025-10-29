from django.contrib import admin
from .models import User, Patient, Doctor, Specialization, Appointment, AppointmentType

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=("username","email","account_type","is_staff","is_active")
    list_filter=("account_type","is_staff","is_active")
    search_fields=("username","email")

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("imie", "nazwisko", "pesel", "telefon")
    search_fields = ("imie", "nazwisko", "pesel")

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("imie", "nazwisko", "specjalizacja", "telefon")
    list_filter = ("specjalizacja",)
    search_fields = ("imie", "nazwisko")

@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(AppointmentType)
class AppointmentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'specialization','type','date','time','status')
    list_filter = ('specialization','status','date', 'type')
    search_fields = ('patient_imie', 'patient_nazwisko', 'doctor_imie', 'doctor_nazwisko')

# Register your models here.
