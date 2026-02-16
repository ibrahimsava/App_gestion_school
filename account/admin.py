from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Student, Parent, Teacher

# ==================== ACCOUNT ADMIN ====================

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'get_full_name', 'user_type', 'phone', 'email']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    list_filter = ['user_type', 'date_joined']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Extended Info', {'fields': ('user_type', 'phone', 'address', 'profile_picture', 'date_of_birth')}),
    )
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Full Name'


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'admission_number', 'current_class', 'is_active', 'admission_date']
    search_fields = ['user__username', 'admission_number', 'user__first_name', 'user__last_name']
    list_filter = ['current_class', 'is_active', 'admission_date']
    readonly_fields = ['admission_date']
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Full Name'


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'get_email', 'occupation', 'get_children_count']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name']
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Full Name'
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'
    
    def get_children_count(self, obj):
        return obj.children.count()
    get_children_count.short_description = 'Children Count'


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'employee_id', 'joining_date', 'qualification', 'is_class_teacher']
    search_fields = ['user__username', 'employee_id', 'user__first_name', 'user__last_name']
    list_filter = ['is_class_teacher', 'joining_date']
    filter_horizontal = ['subjects']
    readonly_fields = ['joining_date']
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Full Name'
