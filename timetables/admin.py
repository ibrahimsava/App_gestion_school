from django.contrib import admin
from .models import Timetable

# ==================== TIMETABLES ADMIN ====================

@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ['class_obj', 'subject', 'teacher', 'day', 'start_time', 'end_time', 'room_number', 'is_active']
    search_fields = ['class_obj__name', 'subject__name', 'teacher__user__username']
    list_filter = ['day', 'class_obj', 'subject', 'is_active']
    ordering = ['day', 'start_time']
