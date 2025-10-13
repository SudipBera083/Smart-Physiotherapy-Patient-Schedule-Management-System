from django.db import models

class Patient(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('Regular', 'Regular'),
        ('Critical', 'Critical'),
    ]
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    medical_notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='New')
    total_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    pending_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Attended', 'Attended'),
        ('Absent', 'Absent'),
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    fee_paid = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    fee_due = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.patient.name} - {self.date} {self.time}"

class PaymentHistory(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.appointment.patient.name} - {self.amount_paid}"
