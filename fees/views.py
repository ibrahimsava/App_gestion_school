from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import FeeStructure, StudentFee, Payment
from account.models import Student

# ==================== FEES DASHBOARD ====================

class FeesDashboardView(LoginRequiredMixin, TemplateView):
    """Fees dashboard"""
    template_name = 'fees/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_fee_structures'] = FeeStructure.objects.count()
        context['total_payments'] = Payment.objects.count()
        context['pending_fees'] = StudentFee.objects.filter(is_paid=False).count()
        return context


# ==================== FEE STRUCTURE VIEWS ====================

class FeeStructureListView(LoginRequiredMixin, ListView):
    """List fee structures"""
    model = FeeStructure
    template_name = 'fees/fee_structure_list.html'
    paginate_by = 20


class FeeStructureCreateView(LoginRequiredMixin, CreateView):
    """Create fee structure"""
    model = FeeStructure
    template_name = 'fees/fee_structure_form.html'
    fields = ['class_obj', 'fee_type', 'amount', 'due_date', 'is_active']
    success_url = reverse_lazy('fees:fee_structure_list')


# ==================== STUDENT FEE VIEWS ====================

class StudentFeeListView(LoginRequiredMixin, ListView):
    """List fees for a student"""
    model = StudentFee
    template_name = 'fees/student_fees.html'
    paginate_by = 10
    
    def get_queryset(self):
        student_id = self.kwargs.get('student_id')
        return StudentFee.objects.filter(student_id=student_id).select_related('fee_structure')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student'] = get_object_or_404(Student, pk=self.kwargs.get('student_id'))
        return context


# ==================== PAYMENT VIEWS ====================

class PaymentListView(LoginRequiredMixin, ListView):
    """List all payments"""
    model = Payment
    template_name = 'fees/payment_list.html'
    paginate_by = 20
    ordering = ['-payment_date']


class PaymentDetailView(LoginRequiredMixin, DetailView):
    """Payment detail view"""
    model = Payment
    template_name = 'fees/payment_detail.html'


class PaymentCreateView(LoginRequiredMixin, CreateView):
    """Record a payment"""
    model = Payment
    template_name = 'fees/payment_form.html'
    fields = ['student', 'student_fee', 'amount', 'payment_method', 'transaction_id', 'remarks']
    success_url = reverse_lazy('fees:payment_list')
    
    def form_valid(self, form):
        form.instance.recorded_by = self.request.user
        return super().form_valid(form)
