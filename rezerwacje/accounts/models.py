from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta, datetime
from django.core.validators import FileExtensionValidator

class User(AbstractUser):
    ACCOUNT_TYPES = [
        ('patient', 'Pacjent'),
        ('doctor', "Lekarz"),
        ('admin', 'Administrator'),
    ]
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES, default='patient')

    def __str__(self):
        return f"{self.username} ({self.get_account_type_display()})"

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="patient_profile")
    pesel = models.CharField(max_length=11, unique=True)
    imie = models.CharField(max_length=50)
    nazwisko = models.CharField(max_length=50, blank=True)
    data_urodzenia = models.DateField(blank=True, null=True)
    telefon = models.CharField(max_length=20, blank=True)
    adres = models.TextField(blank=True)

    def __str__(self):
        return f"{self.imie} {self.nazwisko} (PESEL: {self.pesel})"

class Specialization(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Specjalizacja"
        verbose_name_plural = "Specjalizacje"
    
    def __str__(self):
        return self.name
    
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor_profile")
    pesel = models.CharField(max_length=11, unique=True)
    imie = models.CharField(max_length=50)
    nazwisko = models.CharField(max_length=50)
    telefon = models.CharField(max_length=20, blank=True)
    specjalizacja = models.ForeignKey(Specialization, on_delete=models.PROTECT, related_name="doctors")

    def __str__(self):
        return f"Dr {self.imie} {self.nazwisko} - {self.specjalizacja.name}"

class AppointmentType(models.Model):
    name=models.CharField(max_length=100, unique=True, verbose_name="Nazwa typu wizyty")
    description = models.TextField(blank=True, null=True, verbose_name="Opis")

    class Meta:
        verbose_name = "Typ wizyty"
        verbose_name_plural = "Typy wizyt"
    
    def __str__(self):
        return self.name

class Appointment(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="appointments",
        verbose_name="Pacjent"
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="appointments",
        verbose_name="Lekarz"
    )
    specialization = models.ForeignKey(
        Specialization,
        on_delete=models.PROTECT,
        verbose_name="Specjalizacja"
    )

    type = models.ForeignKey(
        AppointmentType,
        on_delete=models.PROTECT,
        verbose_name="Typ wizyty"
    )

    date=models.DateField(verbose_name="Data wizyty")
    time=models.TimeField(verbose_name="Godzina wizyty")

    STATUS_CHOICES = [
        ('scheduled', 'Zaplanowana'),
        ('canceled', 'Odwołana'),
        ('completed', 'Zakończona'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='scheduled',
        verbose_name="Status wizyty"
    )
    notes=models.TextField(
        blank=True,
        null=True,
        verbose_name="Uwagi do wizyty"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data utworzenia")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data aktualizacji")
    class Meta:
        verbose_name="Wizyta"
        verbose_name_plural="Wizyty"
        ordering = ['date','time']

    def clean(self):
        if self.doctor:
            start_time=(timezone.datetime.combine(self.date, self.time) - timedelta(minutes=30)).time()
            end_time = (timezone.datetime.combine(self.date, self.time)+timedelta(minutes=30)).time()

            conflict = Appointment.objects.filter(
                doctor=self.doctor,
                date=self.date,
                time__gte=start_time,
                time__lte=end_time
            ).exclude(pk=self.pk)

            if conflict.exists():
                raise ValidationError("Ten lekarz ma już wizytę w tym terminie lub w ciągu 30 minut przed/po.")
    
    def can_modify(self):
        now=timezone.localtime()
        appointment_datetime=timezone.make_aware(
            datetime.combine(self.date, self.time),
            timezone.get_current_timezone()
        )
        return appointment_datetime - now >= timedelta(hours=24)

    def __str__(self):
        return f"Wizyta {self.date} {self.time} - {self.patient.imie} {self.patient.nazwisko} u {self.doctor if self.doctor else 'nieprzydzielony.'}"
    
class VisitSummary(models.Model):
    appointment=models.OneToOneField(
        'Appointment',
        on_delete=models.CASCADE,
        related_name='summary'
    )
    prescription=models.TextField(verbose_name="Recepta", blank=True, null=True)
    recommendations=models.TextField(verbose_name="Zalecenia", blank=True, null=True)
    created_at=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Podsumowanie wizyty {self.appointment.id} - {self.appointment.patient.imie} {self.appointment.patient.nazwisko}"
    
class LeaveRequest(models.Model):
    LEAVE_TYPES=[
        ('on_demand', 'Na żądanie'),
        ('sick_leave', 'Chorobowe'),
    ]

    STATUS_CHOICES = [
        ('pending','Oczekuje na akceptację'),
        ('approved','Zatwierdzone'),
        ('rejected','Odrzucone'),
    ]

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='leave_requests',
        verbose_name='Lekarz'
    )
    leave_type = models.CharField(
        max_length=20,
        choices=LEAVE_TYPES,
        verbose_name="Typ wolnego"
    )

    start_date=models.DateField(verbose_name="Początek wolnego")
    end_date=models.DateField(verbose_name="Koniec wolnego")

    document=models.FileField(
        upload_to='leave_documents/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf','jpg','jpeg','png'])],
        verbose_name="Załącznik (dla chorobowego)"
    )

    status=models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Status"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data złożenia wniosku")
    updated_at=models.DateTimeField(auto_now=True, verbose_name="Data aktualizacji")

    class Meta:
        verbose_name="Wniosek o wolne"
        verbose_name_plural="Wnioski o wolne"
        ordering=['-created_at']
    
    def __str__(self):
        return f"{self.get_leave_type_display()} - {self.doctor.imie} {self.doctor.nazwisko} ({self.get_status_display()})"
    
    def clean(self):
        """
        Walidacja:
        - Na żądanie: min 48h wyprzedzenia
        - Chorobowe: wymagany załącznik
        - Zakres dat: start <= end 
        """

        from django.core.exceptions import ValidationError
        now = timezone.localtime().date()

        if self.leave_type == 'on_demand' and (self.start_date - now).days < 2:
            raise ValidationError("Wniosek na żądanie musi być złożony z co najmniej 48-godzinnym wyprzedzeniem.")
        if self.leave_type == 'sick_leave' and not self.document:
            raise ValidationError("Dla chorobowego musisz załączyć plik potwierdzający zwolnienie.")
        if self.start_date > self.end_date:
            raise ValidationError("Data zakończonego wolnego nie może być wcześniej niż data rozpoczęcia.")