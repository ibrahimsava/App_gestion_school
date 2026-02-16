from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Message, Announcement, Notification

# ==================== COMMUNICATIONS DASHBOARD ====================

class CommunicationsDashboardView(LoginRequiredMixin, TemplateView):
    """Communications dashboard"""
    template_name = 'communications/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['unread_messages'] = Message.objects.filter(recipient=user, is_read=False).count()
        context['unread_notifications'] = Notification.objects.filter(user=user, is_read=False).count()
        context['active_announcements'] = Announcement.objects.filter(is_active=True).count()
        return context


# ==================== MESSAGE VIEWS ====================

class MessageListView(LoginRequiredMixin, ListView):
    """List received messages"""
    model = Message
    template_name = 'communications/message_list.html'
    paginate_by = 20
    
    def get_queryset(self):
        return Message.objects.filter(recipient=self.request.user).select_related('sender').order_by('-created_at')


class MessageDetailView(LoginRequiredMixin, DetailView):
    """Message detail view"""
    model = Message
    template_name = 'communications/message_detail.html'
    
    def get_object(self):
        obj = super().get_object()
        if obj.recipient == self.request.user and not obj.is_read:
            obj.is_read = True
            obj.read_at = __import__('django.utils.timezone', fromlist=['now']).now()
            obj.save()
        return obj


class MessageCreateView(LoginRequiredMixin, CreateView):
    """Send message"""
    model = Message
    template_name = 'communications/message_form.html'
    fields = ['recipient', 'subject', 'content']
    success_url = reverse_lazy('communications:message_list')
    
    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super().form_valid(form)


# ==================== ANNOUNCEMENT VIEWS ====================

class AnnouncementListView(LoginRequiredMixin, ListView):
    """List announcements"""
    model = Announcement
    template_name = 'communications/announcement_list.html'
    paginate_by = 10
    
    def get_queryset(self):
        return Announcement.objects.filter(is_active=True).select_related('created_by').order_by('-published_date')


class AnnouncementDetailView(LoginRequiredMixin, DetailView):
    """Announcement detail view"""
    model = Announcement
    template_name = 'communications/announcement_detail.html'


# ==================== NOTIFICATION VIEWS ====================

class NotificationListView(LoginRequiredMixin, ListView):
    """List user notifications"""
    model = Notification
    template_name = 'communications/notification_list.html'
    paginate_by = 20
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')


class NotificationMarkReadView(LoginRequiredMixin, DetailView):
    """Mark notification as read"""
    model = Notification
    
    def get_object(self):
        obj = super().get_object()
        if not obj.is_read:
            obj.is_read = True
            obj.read_at = __import__('django.utils.timezone', fromlist=['now']).now()
            obj.save()
        return obj
    
    def get(self, request, *args, **kwargs):
        self.get_object()
        return redirect('communications:notification_list')
