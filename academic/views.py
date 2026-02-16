from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Subject, Class, Exam, ExamResult

# ==================== ACADEMIC DASHBOARD ====================

class AcademicDashboardView(LoginRequiredMixin, TemplateView):
    """Academic dashboard"""
    template_name = 'academic/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_subjects'] = Subject.objects.count()
        context['total_classes'] = Class.objects.count()
        context['total_exams'] = Exam.objects.count()
        return context


# ==================== SUBJECT VIEWS ====================

class SubjectListView(LoginRequiredMixin, ListView):
    """List all subjects"""
    model = Subject
    template_name = 'academic/subject_list.html'
    paginate_by = 20


class SubjectDetailView(LoginRequiredMixin, DetailView):
    """Subject detail view"""
    model = Subject
    template_name = 'academic/subject_detail.html'


class SubjectCreateView(LoginRequiredMixin, CreateView):
    """Create subject"""
    model = Subject
    template_name = 'academic/subject_form.html'
    fields = ['name', 'code', 'description']
    success_url = reverse_lazy('academic:subject_list')


class SubjectUpdateView(LoginRequiredMixin, UpdateView):
    """Update subject"""
    model = Subject
    template_name = 'academic/subject_form.html'
    fields = ['name', 'code', 'description']
    success_url = reverse_lazy('academic:subject_list')


class SubjectDeleteView(LoginRequiredMixin, DeleteView):
    """Delete subject"""
    model = Subject
    template_name = 'academic/subject_confirm_delete.html'
    success_url = reverse_lazy('academic:subject_list')


# ==================== CLASS VIEWS ====================

class ClassListView(LoginRequiredMixin, ListView):
    """List all classes"""
    model = Class
    template_name = 'academic/class_list.html'
    paginate_by = 20
    ordering = ['level', 'section']


class ClassDetailView(LoginRequiredMixin, DetailView):
    """Class detail view"""
    model = Class
    template_name = 'academic/class_detail.html'
    context_object_name = 'class_obj'


class ClassCreateView(LoginRequiredMixin, CreateView):
    """Create class"""
    model = Class
    template_name = 'academic/class_form.html'
    fields = ['name', 'code', 'level', 'section', 'subjects']
    success_url = reverse_lazy('academic:class_list')


# ==================== EXAM VIEWS ====================

class ExamListView(LoginRequiredMixin, ListView):
    """List all exams"""
    model = Exam
    template_name = 'academic/exam_list.html'
    paginate_by = 20
    ordering = ['-exam_date']


class ExamDetailView(LoginRequiredMixin, DetailView):
    """Exam detail view"""
    model = Exam
    template_name = 'academic/exam_detail.html'


class ExamCreateView(LoginRequiredMixin, CreateView):
    """Create exam"""
    model = Exam
    template_name = 'academic/exam_form.html'
    fields = ['name', 'exam_type', 'class_obj', 'subject', 'exam_date', 'exam_time', 'total_marks', 'passing_marks', 'duration_minutes']
    success_url = reverse_lazy('academic:exam_list')


# ==================== EXAM RESULT VIEWS ====================

class ExamResultListView(LoginRequiredMixin, ListView):
    """List exam results"""
    model = ExamResult
    template_name = 'academic/result_list.html'
    paginate_by = 20
    ordering = ['-created_at']

