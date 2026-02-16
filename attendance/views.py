from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Attendance, AttendanceReport
from account.models import Student
from academic.models import Class

# ==================== ATTENDANCE DASHBOARD ====================

class AttendanceDashboardView(LoginRequiredMixin, TemplateView):
    """Attendance dashboard"""
    template_name = 'attendance/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_attendances'] = Attendance.objects.count()
        context['total_reports'] = AttendanceReport.objects.count()
        return context


# ==================== MARK ATTENDANCE ====================

class MarkAttendanceView(LoginRequiredMixin, TemplateView):
    """Mark attendance view"""
    template_name = 'attendance/mark_attendance.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['classes'] = Class.objects.all()
        return context


# ==================== CLASS ATTENDANCE ====================

class ClassAttendanceView(LoginRequiredMixin, ListView):
    """View attendance for a class"""
    model = Attendance
    template_name = 'attendance/class_attendance.html'
    paginate_by = 20
    
    def get_queryset(self):
        class_id = self.kwargs.get('class_id')
        return Attendance.objects.filter(class_obj_id=class_id).select_related('student', 'recorded_by')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['class_obj'] = get_object_or_404(Class, pk=self.kwargs.get('class_id'))
        return context


# ==================== ATTENDANCE REPORT ====================

class AttendanceReportView(LoginRequiredMixin, ListView):
    """Student attendance report"""
    model = AttendanceReport
    template_name = 'attendance/report.html'
    paginate_by = 12
    
    def get_queryset(self):
        student_id = self.kwargs.get('student_id')
        return AttendanceReport.objects.filter(student_id=student_id).order_by('-year', '-month')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student'] = get_object_or_404(Student, pk=self.kwargs.get('student_id'))
        return context
