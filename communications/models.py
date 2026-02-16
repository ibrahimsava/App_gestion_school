from django.db import models

# Create your models here.

# ==================== COMMUNICATIONS APP ====================

class Message(models.Model):
    """Direct message model"""
    sender = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Messages'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.sender.get_full_name()} to {self.recipient.get_full_name()}: {self.subject}"


class Announcement(models.Model):
    """Announcement model"""
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='low')
    created_by = models.ForeignKey('account.User', on_delete=models.SET_NULL, null=True, related_name='announcements')
    target_class = models.ForeignKey('academic.Class', on_delete=models.CASCADE, null=True, blank=True, related_name='announcements')
    is_active = models.BooleanField(default=True)
    published_date = models.DateTimeField(auto_now_add=True)
    expires_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name_plural = 'Announcements'
        ordering = ['-published_date']
    
    def __str__(self):
        return self.title


class Notification(models.Model):
    """Notification model"""
    NOTIFICATION_TYPES = (
        ('assignment', 'Assignment'),
        ('announcement', 'Announcement'),
        ('exam', 'Exam'),
        ('event', 'Event'),
        ('message', 'Message'),
        ('other', 'Other'),
    )
    
    user = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.get_full_name()}"
