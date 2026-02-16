from django.db import models

# Create your models here.

# ==================== FEES APP ====================

class FeeStructure(models.Model):
    """Fee Structure model"""
    class_obj = models.ForeignKey('academic.Class', on_delete=models.CASCADE, related_name='fee_structures')
    fee_type = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Fee Structures'
        unique_together = ('class_obj', 'fee_type')
    
    def __str__(self):
        return f"{self.class_obj} - {self.fee_type} ({self.amount})"


class StudentFee(models.Model):
    """Student Fee Tracker model"""
    student = models.ForeignKey('account.Student', on_delete=models.CASCADE, related_name='student_fees')
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    due_date = models.DateField()
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Student Fees'
        unique_together = ('student', 'fee_structure')
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.fee_structure.fee_type}"
    
    @property
    def remaining_balance(self):
        return self.amount_due - self.amount_paid


class Payment(models.Model):
    """Payment model"""
    PAYMENT_METHODS = (
        ('cash', 'Cash'),
        ('check', 'Check'),
        ('online', 'Online Transfer'),
        ('card', 'Card'),
    )
    
    student = models.ForeignKey('account.Student', on_delete=models.CASCADE, related_name='payments')
    student_fee = models.ForeignKey(StudentFee, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    transaction_id = models.CharField(max_length=100, blank=True, unique=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True)
    recorded_by = models.ForeignKey('account.User', on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name_plural = 'Payments'
        ordering = ['-payment_date']
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.amount} on {self.payment_date.date()}"
