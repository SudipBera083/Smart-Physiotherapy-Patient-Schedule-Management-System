from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from datetime import date
from django.db.models import Sum, Count
from .models import Patient, Appointment, PaymentHistory
from .utils import suggest_next_slot, missed_patients, frequent_time_slot

# -----------------------------
# Dashboard View
# -----------------------------
def dashboard(request):
    today = timezone.localdate()

    # Today's appointments
    todays_appointments = Appointment.objects.filter(date=today).order_by('time')

    # Upcoming appointments (next 7 days)
    upcoming_appointments = Appointment.objects.filter(date__gt=today).order_by('date', 'time')[:7]

    # Pending Payments
    pending_payments = Appointment.objects.filter(fee_due__gt=0).order_by('date')

    # Missed / Absent today
    missed_appointments = Appointment.objects.filter(date=today, status='Absent')

    # Smart recommendation: patients who missed today
    missed_today = missed_patients()

    context = {
        'todays_appointments': todays_appointments,
        'upcoming_appointments': upcoming_appointments,
        'pending_payments': pending_payments,
        'missed_appointments': missed_appointments,
        'missed_today': missed_today,
    }
    return render(request, 'dashboard.html', context)

# -----------------------------
# Patients List View
# -----------------------------
def patients(request):
    patients = Patient.objects.all()
    return render(request, 'patients.html', {'patients': patients})

# -----------------------------
# Add Appointment View
# -----------------------------
def add_appointment(request):
    patients = Patient.objects.all()  # for dropdown

    if request.method == "POST":
        patient_id = request.POST.get('patient')
        date_val = request.POST.get('date')
        time_val = request.POST.get('time')
        fee_paid = float(request.POST.get('fee_paid', 0))

        patient = Patient.objects.get(id=patient_id)
        fee_due = max(patient.total_fee - fee_paid, 0)

        # Create appointment
        appointment = Appointment.objects.create(
            patient=patient,
            date=date_val,
            time=time_val,
            fee_paid=fee_paid,
            fee_due=fee_due,
        )

        # Update patient's pending_fee
        patient.pending_fee = fee_due
        patient.save()

        messages.success(request, f"Appointment added for {patient.name}")
        return redirect('dashboard')

    # GET request → show form with smart time suggestion
    suggested_times = {}
    for patient in patients:
        # Either use frequent time or next free slot
        suggested_times[patient.id] = frequent_time_slot(patient.id) or suggest_next_slot(patient.id)

    context = {
        'patients': patients,
        'suggested_times': suggested_times
    }
    return render(request, 'add_appointment.html', context)

# -----------------------------
# Mark Attendance
# -----------------------------
def mark_attendance(request, appointment_id, status):
    """
    status = 'Attended' or 'Absent'
    """
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = status
    appointment.save()
    messages.success(request, f"Marked {appointment.patient.name} as {status}")
    return redirect('dashboard')

# -----------------------------
# Collect Partial Payment
# -----------------------------
def collect_payment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == "POST":
        amount = float(request.POST.get('amount', 0))
        if amount <= 0:
            messages.error(request, "Invalid amount")
            return redirect('dashboard')

        # Update appointment fee_paid and fee_due
        appointment.fee_paid += amount
        appointment.fee_due = max(appointment.fee_due - amount, 0)
        appointment.save()

        # Update patient pending fee
        patient = appointment.patient
        patient.pending_fee = appointment.fee_due
        patient.save()

        # Record payment history
        PaymentHistory.objects.create(
            appointment=appointment,
            amount_paid=amount
        )

        messages.success(request, f"Collected ₹{amount} from {patient.name}")
        return redirect('dashboard')

    # GET → Show simple input form
    return render(request, 'collect_payment.html', {'appointment': appointment})


def reports(request):
    today = timezone.localdate()

    # Total collected payments
    total_collected = Appointment.objects.aggregate(total=Sum('fee_paid'))['total'] or 0

    # Total pending fees
    total_pending = Appointment.objects.aggregate(total=Sum('fee_due'))['total'] or 0

    # Total appointments
    total_appointments = Appointment.objects.count()

    # Missed appointments
    total_missed = Appointment.objects.filter(status='Absent').count()

    # Most frequent patient slots
    patient_slots = []
    patients = Patient.objects.all()
    for patient in patients:
        slot = frequent_time_slot(patient.id)
        patient_slots.append({
            'patient': patient.name,
            'slot': slot
        })

    context = {
        'total_collected': total_collected,
        'total_pending': total_pending,
        'total_appointments': total_appointments,
        'total_missed': total_missed,
        'patient_slots': patient_slots,
    }

    return render(request, 'reports.html', context)
