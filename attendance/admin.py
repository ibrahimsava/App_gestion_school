from django.contrib import admin
from .models import Attendance, AttendanceReport

# ==================== ATTENDANCE ADMIN ====================

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'date', 'status', 'class_obj', 'recorded_by']
    search_fields = ['student__user__username', 'date']
    list_filter = ['status', 'date', 'class_obj']
    readonly_fields = ['created_at']
    ordering = ['-date']


@admin.register(AttendanceReport)
class AttendanceReportAdmin(admin.ModelAdmin):
    list_display = ['student', 'month', 'year', 'attendance_percentage', 'present_days', 'absent_days']
    search_fields = ['student__user__username']
    list_filter = ['month', 'year']
    readonly_fields = ['generated_date']
