from django.contrib import admin
from .models import Message, Announcement, Notification

# ==================== COMMUNICATIONS ADMIN ====================

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'recipient', 'subject', 'is_read', 'created_at']
    search_fields = ['sender__username', 'recipient__username', 'subject']
    list_filter = ['is_read', 'created_at']
    readonly_fields = ['created_at', 'read_at']
    ordering = ['-created_at']


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'priority', 'created_by', 'target_class', 'is_active', 'published_date']
    search_fields = ['title', 'content']
    list_filter = ['priority', 'is_active', 'published_date']
    readonly_fields = ['published_date']
    ordering = ['-published_date']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'notification_type', 'is_read', 'created_at']
    search_fields = ['user__username', 'title', 'message']
    list_filter = ['notification_type', 'is_read', 'created_at']
    readonly_fields = ['created_at', 'read_at']
    ordering = ['-created_at']
