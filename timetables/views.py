from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Timetable
from academic.models import Class

# ==================== TIMETABLE DASHBOARD ====================

class TimetableDashboardView(LoginRequiredMixin, TemplateView):
    """Timetable dashboard"""
    template_name = 'timetables/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_timetables'] = Timetable.objects.filter(is_active=True).count()
        context['classes'] = Class.objects.all()
        return context


# ==================== CLASS TIMETABLE VIEW ====================

class ClassTimetableView(LoginRequiredMixin, ListView):
    """View timetable for a specific class"""
    model = Timetable
    template_name = 'timetables/class_timetable.html'
    paginate_by = 50
    
    def get_queryset(self):
        class_id = self.kwargs.get('class_id')
        return Timetable.objects.filter(class_obj_id=class_id, is_active=True).select_related('subject', 'teacher').order_by('day', 'start_time')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['class_obj'] = get_object_or_404(Class, pk=self.kwargs.get('class_id'))
        return context


# ==================== TIMETABLE MANAGEMENT VIEWS ====================

class TimetableCreateView(LoginRequiredMixin, CreateView):
    """Create timetable entry"""
    model = Timetable
    template_name = 'timetables/timetable_form.html'
    fields = ['class_obj', 'subject', 'teacher', 'day', 'start_time', 'end_time', 'room_number', 'is_active']
    success_url = reverse_lazy('timetables:dashboard')


class TimetableUpdateView(LoginRequiredMixin, UpdateView):
    """Update timetable entry"""
    model = Timetable
    template_name = 'timetables/timetable_form.html'
    fields = ['class_obj', 'subject', 'teacher', 'day', 'start_time', 'end_time', 'room_number', 'is_active']
    success_url = reverse_lazy('timetables:dashboard')


class TimetableDeleteView(LoginRequiredMixin, DeleteView):
    """Delete timetable entry"""
    model = Timetable
    template_name = 'timetables/timetable_confirm_delete.html'
    success_url = reverse_lazy('timetables:dashboard')
