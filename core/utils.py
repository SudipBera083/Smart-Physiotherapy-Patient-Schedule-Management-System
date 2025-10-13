from datetime import timedelta, datetime
from django.utils import timezone
from django.db.models import Count
from .models import Appointment

def suggest_next_slot(patient_id=None):
    today = timezone.localdate()
    working_start = datetime.strptime("09:00", "%H:%M").time()
    working_end = datetime.strptime("17:00", "%H:%M").time()
    slot_duration = timedelta(minutes=30)

    todays_appointments = Appointment.objects.filter(date=today).order_by('time')

    if patient_id:
        last_appt = Appointment.objects.filter(patient_id=patient_id).order_by('-date', '-time').first()
        if last_appt and last_appt.date < today:
            preferred_time = last_appt.time
            if not todays_appointments.filter(time=preferred_time).exists():
                return preferred_time

    current_time = working_start
    while current_time < working_end:
        if not todays_appointments.filter(time=current_time).exists():
            return current_time
        current_time = (datetime.combine(today, current_time) + slot_duration).time()

    tomorrow = today + timedelta(days=1)
    return working_start, tomorrow


def missed_patients():
    today = timezone.localdate()
    missed_today = Appointment.objects.filter(date=today, status='Absent')
    return [appt.patient for appt in missed_today]


def frequent_time_slot(patient_id):
    times = Appointment.objects.filter(patient_id=patient_id)\
        .values('time')\
        .annotate(count=Count('time'))\
        .order_by('-count')
    if times:
        return times[0]['time']
    return None
