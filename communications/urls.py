from django.urls import path
from . import views

app_name = 'communications'

urlpatterns = [
    path('', views.CommunicationsDashboardView.as_view(), name='dashboard'),
    path('messages/', views.MessageListView.as_view(), name='message_list'),
    path('message/<int:pk>/', views.MessageDetailView.as_view(), name='message_detail'),
    path('message/send/', views.MessageCreateView.as_view(), name='message_send'),
    path('announcements/', views.AnnouncementListView.as_view(), name='announcement_list'),
    path('announcement/<int:pk>/', views.AnnouncementDetailView.as_view(), name='announcement_detail'),
    path('notification/<int:pk>/read/', views.NotificationMarkReadView.as_view(), name='notification_read'),
    path('notifications/', views.NotificationListView.as_view(), name='notification_list'),
]
