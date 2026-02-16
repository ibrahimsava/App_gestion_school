from django.urls import path
from . import views

app_name = 'timetables'

urlpatterns = [
    path('', views.TimetableDashboardView.as_view(), name='dashboard'),
    path('class/<int:class_id>/', views.ClassTimetableView.as_view(), name='class_timetable'),
    path('create/', views.TimetableCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.TimetableUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.TimetableDeleteView.as_view(), name='delete'),
]
