from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


# ==================== ACCOUNTS APP ====================

class User(AbstractUser):
    """Extended user model for all users"""
    USER_TYPES = (
        ('student', 'Student'),
        ('parent', 'Parent'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    class Meta:
        db_table = 'account_user'
    
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='account_user_groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='account_user_permissions'
    )
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.user_type})"


class Student(models.Model):
    """Student profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    admission_number = models.CharField(max_length=20, unique=True)
    admission_date = models.DateField()
    current_class = models.ForeignKey('academic.Class', on_delete=models.SET_NULL, null=True, related_name='students')
    parent = models.ForeignKey('Parent', on_delete=models.SET_NULL, null=True, related_name='children')
    blood_group = models.CharField(max_length=5, blank=True)
    emergency_contact = models.CharField(max_length=15, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.admission_number}"


class Parent(models.Model):
    """Parent profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_profile')
    occupation = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.user.get_full_name()


class Teacher(models.Model):
    """Teacher profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    employee_id = models.CharField(max_length=20, unique=True)
    joining_date = models.DateField()
    qualification = models.CharField(max_length=200)
    subjects = models.ManyToManyField('academic.Subject', related_name='teachers')
    is_class_teacher = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.employee_id}"
