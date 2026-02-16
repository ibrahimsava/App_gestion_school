from django.contrib import admin
from .models import Subject, Class, Exam, ExamResult, ClassSchedule

# ==================== ACADEMIC ADMIN ====================

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name', 'code']
    ordering = ['name']


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'level', 'section']
    search_fields = ['name', 'code']
    list_filter = ['level', 'section']
    filter_horizontal = ['subjects']
    ordering = ['level', 'section']


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['name', 'exam_type', 'class_obj', 'subject', 'exam_date', 'total_marks']
    search_fields = ['name', 'class_obj__name']
    list_filter = ['exam_type', 'exam_date', 'class_obj']
    ordering = ['-exam_date']


@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam', 'marks_obtained', 'percentage', 'grade']
    search_fields = ['student__user__username', 'exam__name']
    list_filter = ['exam', 'grade']
    readonly_fields = ['created_at']


@admin.register(ClassSchedule)
class ClassScheduleAdmin(admin.ModelAdmin):
    list_display = ['class_obj', 'subject', 'teacher', 'day', 'start_time', 'end_time', 'room_number']
    search_fields = ['class_obj__name', 'subject__name', 'teacher__user__username']
    list_filter = ['day', 'class_obj', 'subject']
