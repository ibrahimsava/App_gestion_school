from django.urls import path
from . import views

app_name = 'academic'

urlpatterns = [
    path('', views.AcademicDashboardView.as_view(), name='dashboard'),
    path('subjects/', views.SubjectListView.as_view(), name='subject_list'),
    path('subject/create/', views.SubjectCreateView.as_view(), name='subject_create'),
    path('subject/<int:pk>/', views.SubjectDetailView.as_view(), name='subject_detail'),
    path('subject/<int:pk>/update/', views.SubjectUpdateView.as_view(), name='subject_update'),
    path('subject/<int:pk>/delete/', views.SubjectDeleteView.as_view(), name='subject_delete'),
    path('classes/', views.ClassListView.as_view(), name='class_list'),
    path('class/create/', views.ClassCreateView.as_view(), name='class_create'),
    path('class/<int:pk>/', views.ClassDetailView.as_view(), name='class_detail'),
    path('exams/', views.ExamListView.as_view(), name='exam_list'),
    path('exam/create/', views.ExamCreateView.as_view(), name='exam_create'),
    path('exam/<int:pk>/', views.ExamDetailView.as_view(), name='exam_detail'),
    path('results/', views.ExamResultListView.as_view(), name='result_list'),
]
