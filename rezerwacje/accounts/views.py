from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import PatientRegisterForm, LeaveRequestForm, DoctorRegisterForm, AppointmentAdminForm, AppointmentPatientForm, VisitSummaryForm
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Doctor, Appointment, LeaveRequest
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime
from django.db.models import Q

class UserLoginView(LoginView):
    template_name="accounts/login.html"

class UserLogoutView(LogoutView):
    next_page=reverse_lazy("login")

class UserRegisterView(CreateView):
    form_class = PatientRegisterForm
    template_name = "accounts/register.html"
    success_url=reverse_lazy("login")

class DoctorRegisterView(CreateView):
    form_class = DoctorRegisterForm
    template_name = "accounts/doctor_register.html"
    success_url = reverse_lazy("login")

@login_required
def dashboard(request):
    if request.user.account_type == 'patient':
        return redirect('patient_dashboard')
    elif request.user.account_type == 'doctor':
        return redirect('doctor_dashboard')
    elif request.user.account_type == 'admin':
        return redirect('admin_dashboard')
    else:
        return redirect('login')
        
@login_required
def patient_dashboard(request):
    now=timezone.localtime()
    today=now.date()
    current_time=now.time()
    if request.method == "POST":
         form = AppointmentPatientForm(request.POST)
         if form.is_valid():
             appointment = form.save(commit=False)
             appointment.patient = request.user.patient_profile
             appointment.save()
             return redirect('patient_dashboard')
    else:
        form = AppointmentPatientForm()

    upcoming_appointments = Appointment.objects.filter(
        patient=request.user.patient_profile,
        status='scheduled'
    ).filter(
        (Q(date=today, time__gte=current_time) |
         Q(date__gt=today))
    ).select_related('doctor', 'specialization','type').order_by('date','time')

    past_appointments=Appointment.objects.filter(
        patient=request.user.patient_profile,
        status='completed',
        summary__isnull=False
    ).select_related('doctor','specialization','type','summary').order_by('-date','-time')

    return render(request, "dashboards/patient.html",{"form":form, "appointments":upcoming_appointments,"past_appointments":past_appointments})

@login_required
def doctor_dashboard(request):
    if request.user.account_type != 'doctor':
        return redirect('dashboard')
    now=timezone.localtime()
    today=now.date()
    current_time=now.time()
    doctor=request.user.doctor_profile
    doctor_appointments = Appointment.objects.filter(
        doctor=request.user.doctor_profile,
        status='scheduled'
    ).filter(
        (Q(date=today, time__gte=current_time) |
         Q(date__gt=today))
    ).select_related('patient','specialization','type').order_by('date','time')

    if request.method == "POST" and "leave_type" in request.POST:
        leave_form = LeaveRequestForm(request.POST, request.FILES)
        if leave_form.is_valid():
            leave_request = leave_form.save(commit=False)
            leave_request.doctor = doctor
            leave_request.save()
            return redirect('doctor_dashboard')
    else:
        leave_form = LeaveRequestForm()

    leave_requests=LeaveRequest.objects.filter(doctor=doctor).order_by('-created_at')


    return render(request, "dashboards/doctor.html",
                  {
        "leave_form":leave_form,
        "leave_requests":leave_requests,
        "appointments":doctor_appointments,
                  })

    
    

@login_required
def admin_dashboard(request):
    selected_type = request.POST.get("account_type") if request.method == "POST" else None

    form = None
    if selected_type == "patient":
        form = PatientRegisterForm(request.POST or None)
    elif selected_type == "doctor":
        form = DoctorRegisterForm(request.POST or None)

    if form and request.method == "POST" and form.is_valid():
        form.save()
        return redirect("admin_dashboard")

    appointment_form = AppointmentAdminForm(request.POST or None)
    if request.method == "POST" and "create_appointment" in request.POST:
        if appointment_form.is_valid():
            appointment_form.save()
            return redirect("admin_dashboard")

    all_appointments = Appointment.objects.select_related(
        'patient', 'doctor', 'specialization', 'type'
    ).order_by('date', 'time')

    leave_requests = LeaveRequest.objects.select_related('doctor').order_by('-created_at')

    if not form and selected_type is None:
        form = PatientRegisterForm()

    return render(request, "dashboards/admin.html", {
        "form": form,
        "selected_type": selected_type or "",
        "appointment_form": appointment_form,
        "all_appointments": all_appointments,
        "leave_requests": leave_requests,
    })


@login_required
def approve_leave(request, leave_id):
    leave = get_object_or_404(LeaveRequest, id=leave_id)
    leave.status = "approved"
    leave.save()
    return redirect("admin_dashboard")

@login_required
def reject_leave(request, leave_id):
    leave = get_object_or_404(LeaveRequest, id=leave_id)
    leave.status="rejected"
    leave.save()
    return redirect("admin_dashboard")

@login_required
def get_doctors(request):
    specialization_id = request.GET.get('specialization')
    doctors=Doctor.objects.filter(specjalizacja_id=specialization_id)
    data=[{"id":doc.id, "name":f"{doc.imie} {doc.nazwisko}"} for doc in doctors]
    return JsonResponse(data, safe=False)

@login_required
def cancel_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id, patient=request.user.patient_profile)
    if not appointment.can_modify():
        return JsonResponse({"error":"Nie możesz odwołać wizyty później niż 24 godziny przed jej terminem"}, status=400)
    appointment.status="canceled"
    appointment.save()
    return redirect("patient_dashboard")

@login_required
def add_visit_summary(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id, doctor=request.user.doctor_profile)
    if request.method=="POST":
        form=VisitSummaryForm(request.POST)
        if form.is_valid():
            summary = form.save(commit=False)
            summary.appointment = appointment
            summary.save()
            
            appointment.status='completed'
            appointment.save()
            return redirect('doctor_dashboard')
    else:
        form=VisitSummaryForm()

    return render(request, "dashboards/add_summary.html", {
        "form":form,
        "appointment":appointment,
        })

@login_required
def admin_edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == "POST":
        form=AppointmentAdminForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect("admin_dashboard")
    else:
        form=AppointmentAdminForm(instance=appointment)
    return render(request, "dashboards/appointment_edit.html", {
        "form": form,
        "appointment": appointment
    })
@login_required
def admin_delete_appointment(request, appointment_id):
    appointment=get_object_or_404(Appointment, id=appointment_id)
    appointment.delete()
    return redirect("admin_dashboard")

