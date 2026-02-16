from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth import logout
from django.views.generic import TemplateView, ListView, DetailView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import User, Student, Teacher, Parent
from .forms import CustomUserCreationForm
from academic.models import Class, Exam
from communications.models import Notification

# ==================== AUTHENTICATION VIEWS ====================

class LoginView(DjangoLoginView):
    """Login view"""
    template_name = 'account/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        """Redirect to dashboard after successful login"""
        return reverse_lazy('account:dashboard')


class LogoutView(LoginRequiredMixin, View):
    """Logout view"""
    login_url = reverse_lazy('account:login')
    
    def get(self, request):
        """Show logout confirmation page"""
        return render(request, 'account/logout.html')
    
    def post(self, request):
        """Handle logout"""
        logout(request)
        return redirect('account:login')


class RegisterView(CreateView):
    """User registration view"""
    model = User
    template_name = 'account/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('account:login')


# ==================== DASHBOARD VIEWS ====================

class DashboardView(LoginRequiredMixin, TemplateView):
    """Main dashboard view"""
    template_name = 'account/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user_type'] = user.user_type
        
        # Add recent notifications for all users
        context['recent_notifications'] = Notification.objects.filter(user=user).order_by('-created_at')[:5]
        
        if user.user_type == 'student':
            context['student'] = Student.objects.filter(user=user).first()
        elif user.user_type == 'teacher':
            context['teacher'] = Teacher.objects.filter(user=user).first()
        elif user.user_type == 'parent':
            context['parent'] = Parent.objects.filter(user=user).first()
        elif user.user_type == 'admin':
            # Add admin statistics
            context['total_students'] = Student.objects.filter(is_active=True).count()
            context['total_teachers'] = Teacher.objects.count()
            context['total_classes'] = Class.objects.count()
            context['total_exams'] = Exam.objects.count()
            
        return context


class ProfileView(LoginRequiredMixin, DetailView):
    """User profile view"""
    model = User
    template_name = 'account/profile.html'
    
    def get_object(self):
        return self.request.user


# ==================== STUDENT VIEWS ====================

class StudentListView(LoginRequiredMixin, ListView):
    """List all students"""
    model = Student
    template_name = 'account/student_list.html'
    paginate_by = 20
    
    def get_queryset(self):
        return Student.objects.select_related('user', 'current_class').filter(is_active=True)


class StudentDetailView(LoginRequiredMixin, DetailView):
    """Student detail view"""
    model = Student
    template_name = 'account/student_detail.html'
    context_object_name = 'student'


# ==================== TEACHER VIEWS ====================

class TeacherListView(LoginRequiredMixin, ListView):
    """List all teachers"""
    model = Teacher
    template_name = 'account/teacher_list.html'
    paginate_by = 20
    
    def get_queryset(self):
        return Teacher.objects.select_related('user')


# ==================== PARENT VIEWS ====================

class ParentListView(LoginRequiredMixin, ListView):
    """List all parents"""
    model = Parent
    template_name = 'account/parent_list.html'
    paginate_by = 20
    
    def get_queryset(self):
        return Parent.objects.select_related('user')
