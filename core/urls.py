
from django.urls import path
from . import views
urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("patients/", views.patients, name="patients"),
    path('appointments/add/', views.add_appointment, name='add_appointment'),
    path('appointment/<int:appointment_id>/mark/<str:status>/', views.mark_attendance, name='mark_attendance'),
    path('appointment/<int:appointment_id>/payment/', views.collect_payment, name='collect_payment'),

]
