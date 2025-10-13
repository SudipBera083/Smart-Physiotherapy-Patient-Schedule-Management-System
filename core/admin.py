from django.contrib import admin
from .models import Patient, Appointment, PaymentHistory

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact', 'status', 'total_fee', 'pending_fee')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'date', 'time', 'status', 'fee_paid', 'fee_due')

@admin.register(PaymentHistory)
class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'amount_paid', 'payment_date')
