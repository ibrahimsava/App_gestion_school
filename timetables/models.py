from django.db import models

# Create your models here.

# ==================== TIMETABLES APP ====================

class Timetable(models.Model):
    """Timetable model"""
    DAYS = (
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
    )
    
    class_obj = models.ForeignKey('academic.Class', on_delete=models.CASCADE, related_name='timetables')
    subject = models.ForeignKey('academic.Subject', on_delete=models.CASCADE)
    teacher = models.ForeignKey('account.Teacher', on_delete=models.SET_NULL, null=True, blank=True)
    day = models.CharField(max_length=20, choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room_number = models.CharField(max_length=10, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Timetables'
        unique_together = ('class_obj', 'day', 'start_time')
        ordering = ['day', 'start_time']
    
    def __str__(self):
        return f"{self.class_obj} - {self.subject} ({self.day})"
