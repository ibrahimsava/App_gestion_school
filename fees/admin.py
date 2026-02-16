from django.contrib import admin
from .models import FeeStructure, StudentFee, Payment

# ==================== FEES ADMIN ====================

@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ['class_obj', 'fee_type', 'amount', 'due_date', 'is_active']
    search_fields = ['class_obj__name', 'fee_type']
    list_filter = ['is_active', 'class_obj', 'due_date']
    readonly_fields = ['created_at']


@admin.register(StudentFee)
class StudentFeeAdmin(admin.ModelAdmin):
    list_display = ['student', 'fee_structure', 'amount_due', 'amount_paid', 'remaining_balance', 'is_paid', 'due_date']
    search_fields = ['student__user__username', 'fee_structure__fee_type']
    list_filter = ['is_paid', 'due_date', 'fee_structure__class_obj']
    readonly_fields = ['created_at', 'remaining_balance']
    ordering = ['due_date']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['student', 'amount', 'payment_method', 'transaction_id', 'payment_date', 'recorded_by']
    search_fields = ['student__user__username', 'transaction_id']
    list_filter = ['payment_method', 'payment_date']
    readonly_fields = ['payment_date']
    ordering = ['-payment_date']
