
from django.urls import path
from . import views
urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("patients/", views.patients, name="patients"),
    path('patients/add/', views.add_patient, name='add_patient'),
    path('patients/edit/<int:patient_id>/', views.edit_patient, name='edit_patient'),
    path('patients/delete/<int:patient_id>/', views.delete_patient, name='delete_patient'),

    path('appointments/add/', views.add_appointment, name='add_appointment'),
    path('appointment/<int:appointment_id>/mark/<str:status>/', views.mark_attendance, name='mark_attendance'),
    path('appointment/<int:appointment_id>/payment/', views.collect_payment, name='collect_payment'),
    path('reports/', views.reports, name='reports'),
]
