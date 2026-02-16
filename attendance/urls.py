from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('', views.AttendanceDashboardView.as_view(), name='dashboard'),
    path('mark/', views.MarkAttendanceView.as_view(), name='mark_attendance'),
    path('report/<int:student_id>/', views.AttendanceReportView.as_view(), name='report'),
    path('class/<int:class_id>/', views.ClassAttendanceView.as_view(), name='class_attendance'),
]
