from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, LeaveRequest, Patient, Doctor, Specialization, Appointment, AppointmentType, VisitSummary
from django.core.exceptions import ValidationError
from datetime import time, timedelta, datetime, timezone

class PatientRegisterForm(UserCreationForm):
    pesel = forms.CharField(max_length=11, required=True)
    imie = forms.CharField(max_length=50, required=True)
    nazwisko = forms.CharField(max_length=50, required=True)
    data_urodzenia = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    telefon = forms.CharField(max_length=20, required=False)
    adres = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "pesel", "imie", "nazwisko", "data_urodzenia", "telefon", "adres"]

    def clean_pesel(self):
        pesel = self.cleaned_data.get("pesel")
        if Patient.objects.filter(pesel=pesel).exists():
            raise ValidationError("Pacjent z takim numerem PESEL już istnieje.")
        return pesel
    
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Użytkownik o takim loginie już istnieje.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.account_type = "patient"

        if commit:
            user.save()
            Patient.objects.create(
                user=user,
                pesel=self.cleaned_data['pesel'],
                imie=self.cleaned_data['imie'],
                nazwisko=self.cleaned_data['nazwisko'],
                data_urodzenia=self.cleaned_data['data_urodzenia'],
                telefon=self.cleaned_data['telefon'],
                adres=self.cleaned_data['adres']
            )
        return user
    
    

class DoctorRegisterForm(UserCreationForm):
    pesel = forms.CharField(max_length=11, required=True)
    imie = forms.CharField(max_length=50, required=True)
    nazwisko = forms.CharField(max_length=50, required=True)
    telefon = forms.CharField(max_length=20, required=False)
    specjalizacja = forms.ModelChoiceField(
        queryset=Specialization.objects.all(),
        required=True,
        label="Specializacja"
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "pesel", "imie", "nazwisko", "telefon", "specjalizacja"]

    def clean_pesel(self):
        pesel = self.cleaned_data.get("pesel")
        if Doctor.objects.filter(pesel=pesel).exists():
            raise ValidationError("Lekarz z takim numerem PESEL już istnieje.")
        return pesel
    
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Użytkownik o takim loginie już istnieje.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.account_type = "doctor"

        if commit:
            user.save()
            Doctor.objects.create(
                user=user,
                pesel=self.cleaned_data['pesel'],
                imie=self.cleaned_data['imie'],
                nazwisko=self.cleaned_data['nazwisko'],
                telefon=self.cleaned_data['telefon'],
                specjalizacja=self.cleaned_data['specjalizacja']
            )
        return user
    
def generate_time_choices(start="08:00", end="20:00", step=30):
    choices = []
    start_dt = datetime.strptime(start, "%H:%M")
    end_dt = datetime.strptime(end, "%H:%M")
    current = start_dt
    while current<=end_dt:
        choices.append((current.strftime("%H:%M"), current.strftime("%H:%M")))
        current += timedelta(minutes=step)
    return choices

TIME_CHOICES = generate_time_choices()
    
class AppointmentPatientForm(forms.ModelForm):
    time=forms.ChoiceField(
        choices=TIME_CHOICES,
        label="Godzina",
    )

    class Meta:
        model = Appointment
        fields = ['specialization','doctor','type','date','time']
        widgets = { 'date': forms.DateInput(attrs={'type':'date'}),}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset=Doctor.objects.none()
        self.fields['specialization'].label="Specjalizacja"
        self.fields['doctor'].label="Lekarz"
        self.fields['type'].label="Typ wizyty"
        self.fields['date'].label="Data"

        if 'specialization' in self.data:
            try:
                specialization_id = int(self.data.get('specialization'))
                self.fields['doctor'].queryset=Doctor.objects.filter(specjalizacja_id=specialization_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['doctor'].queryset=self.instance.specialization.doctors.all()

        if 'doctor' in self.data and 'date' in self.data:
            doctor_id = self.data.get('doctor')
            date = self.data.get('date')

            if doctor_id and date:
                taken_times = Appointment.objects.filter(
                    doctor_id=doctor_id,
                    date=date
                ).values_list('time',flat=True)

                available_times = [
                    (t, t) for t in dict(TIME_CHOICES).keys() if t not in [str(x) for x in taken_times]
                ]
                self.fields['time'].choices = available_times

    def clean(self):
        cleaned_data = super().clean()
        doctor = cleaned_data.get('doctor')
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')

        if not doctor or not date or not time:
            return cleaned_data
        
        if Appointment.objects.filter(doctor=doctor, date=date, time=time).exists():
            raise forms.ValidationError(
                f"Lekarz {doctor.imie} {doctor.nazwisko} ma już wizytę w tym terminie."
            )
        
        if self.instance.pk:
            patient=self.instance.patient
        else:
            patient=self.initial.get('patient') or self.data.get('patient') or None
        if patient and Appointment.objects.filter(patient=patient, date=date, time=time).exists():
            raise forms.ValidationError("Masz już umówioną wizytę w tym terminie.")
        return cleaned_data


class AppointmentAdminForm(forms.ModelForm):
    time = forms.ChoiceField(
        choices=TIME_CHOICES,
        label="Godzina",
    )

    patient = forms.ModelChoiceField(
        queryset=Patient.objects.all(),
        label="Pacjent",
        widget=forms.Select
    )
    
    class Meta:
        model = Appointment
        fields = ['patient','specialization','doctor','type','date','time']
        widgets = {'date':forms.DateInput(attrs={'type':'date'}),}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset=Doctor.objects.none()
        self.fields['patient'].label_from_instance = lambda obj: f"{obj.imie} {obj.nazwisko} ({obj.pesel})"

        if 'specialization' in self.data:
            try:
                specialization_id = int(self.data.get('specialization'))
                self.fields['doctor'].queryset = Doctor.objects.filter(specjalizacja_id=specialization_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['doctor'].queryset=self.instance.specialization.doctors.all()

        if 'doctor' in self.data and 'date' in self.data:
            doctor_id = self.data.get('doctor')
            date = self.data.get('date')
            if doctor_id and date:
                taken_times=Appointment.objects.filter(
                    doctor_id=doctor_id,
                    date=date
                ).values_list('time',flat=True)
                available_times=[
                    (t,t) for t in dict(TIME_CHOICES).keys() if t not in [str(x) for x in taken_times]
                ]
                self.fields['time'].choices=available_times
    
    def clean(self):
        cleaned_data = super().clean()
        doctor = cleaned_data.get('doctor')
        patient = cleaned_data.get('patient')
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')

        if not doctor or not patient or not date or not time:
            return cleaned_data
        
        if Appointment.objects.filter(doctor=doctor, date=date, time=time).exists():
            raise forms.ValidationError(
                f"Lekarz {doctor.imie} {doctor.nazwisko} ma już wizytę w tym terminie."
            )
        
        if Appointment.objects.filter(patient=patient, date=date, time=time).exists():
            raise forms.ValidationError(
                "Pacjent ma już wizytę w tym terminie."
            )
        return cleaned_data
    
class VisitSummaryForm(forms.ModelForm):
    class Meta:
        model = VisitSummary
        fields = ['prescription','recommendations']
        widgets={
            'prescription': forms.Textarea(attrs={'rows':4}),
            'recommendations':forms.Textarea(attrs={'rows':4}),
        }

class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['leave_type', 'start_date', 'end_date', 'document']
        widgets = {
            'start_date': forms.DateInput(attrs={'type':'date'}),
            'end_date': forms.DateInput(attrs={'type':'date'}),
        }
    def clean(self):
        cleaned_data=super().clean()
        leave_type = cleaned_data.get('leave_type')
        document=cleaned_data.get('document')
        start_date=cleaned_data.get('start_date')
        end_date=cleaned_data.get('end_date')
        
        from django.core.exceptions import ValidationError
        from django.utils import timezone
        now=timezone.localtime().date()

        if leave_type == 'on_demand' and (start_date - now).days < 2:
            raise ValidationError("Wniosek na żądanie musi być złożony z co najmniej 48-godzinnym wyprzedzeniem.")
        if leave_type == 'sick_leave' and not document:
            raise ValidationError("Dla chorobowego musisz załączyć plik potwierdzający zwolnienie.")
        if start_date and end_date and start_date > end_date:
            raise ValidationError("Data zakończenia wolnego nie może być wcześniejsza niż data rozpoczęcia.")
        return cleaned_data