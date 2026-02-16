from django.db import models

# Create your models here.

# ==================== ATTENDANCE APP ====================

class Attendance(models.Model):
    """Attendance model"""
    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('leave', 'Leave'),
    )
    
    student = models.ForeignKey('account.Student', on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    class_obj = models.ForeignKey('academic.Class', on_delete=models.CASCADE, related_name='attendances')
    remarks = models.TextField(blank=True)
    recorded_by = models.ForeignKey('account.Teacher', on_delete=models.SET_NULL, null=True, related_name='recorded_attendances')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Attendances'
        unique_together = ('student', 'date', 'class_obj')
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.date} ({self.status})"


class AttendanceReport(models.Model):
    """Attendance Report model"""
    student = models.ForeignKey('account.Student', on_delete=models.CASCADE, related_name='attendance_reports')
    month = models.IntegerField()  # 1-12
    year = models.IntegerField()
    total_days = models.IntegerField()
    present_days = models.IntegerField()
    absent_days = models.IntegerField()
    late_days = models.IntegerField()
    attendance_percentage = models.FloatField()
    generated_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Attendance Reports'
        unique_together = ('student', 'month', 'year')
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.month}/{self.year}"
