from django.db import models

# Create your models here.

# ==================== ACADEMICS APP ====================

class Subject(models.Model):
    """Subject model"""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = 'Subjects'
    
    def __str__(self):
        return self.name


class Class(models.Model):
    """Class/Grade model"""
    name = models.CharField(max_length=50)  # e.g., "Class 10A", "Grade 9"
    code = models.CharField(max_length=10, unique=True)
    level = models.IntegerField()  # e.g., 10, 9, 8...
    section = models.CharField(max_length=1, blank=True)  # e.g., "A", "B", "C"
    subjects = models.ManyToManyField(Subject, related_name='classes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Classes'
        unique_together = ('level', 'section')
    
    def __str__(self):
        return self.name

     
class Exam(models.Model):
    """Exam model"""
    EXAM_TYPES = (
        ('midterm', 'Mid-Term'),
        ('final', 'Final'),
        ('quiz', 'Quiz'),
        ('practical', 'Practical'),
    )
    
    name = models.CharField(max_length=100)
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPES)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='exams')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exams')
    exam_date = models.DateField()
    exam_time = models.TimeField()
    total_marks = models.IntegerField(default=100)
    passing_marks = models.IntegerField(default=40)
    duration_minutes = models.IntegerField(default=60)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Exams'
        ordering = ['-exam_date']
    
    def __str__(self):
        return f"{self.name} - {self.class_obj}"


class ExamResult(models.Model):
    """Exam Results model"""
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey('account.Student', on_delete=models.CASCADE, related_name='exam_results')
    marks_obtained = models.IntegerField()
    percentage = models.FloatField(null=True, blank=True)
    grade = models.CharField(max_length=2, blank=True)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Exam Results'
        unique_together = ('exam', 'student')
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.exam.name}: {self.marks_obtained}"


class ClassSchedule(models.Model):
    """Class Schedule/Timetable model"""
    DAYS = (
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
    )
    
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='schedules')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey('account.Teacher', on_delete=models.SET_NULL, null=True)
    day = models.CharField(max_length=20, choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room_number = models.CharField(max_length=10, blank=True)
    
    class Meta:
        verbose_name_plural = 'Class Schedules'
        unique_together = ('class_obj', 'day', 'start_time')
    
    def __str__(self):
        return f"{self.class_obj} - {self.subject} ({self.day})"

