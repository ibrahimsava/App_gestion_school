from django.urls import path
from . import views

app_name = 'fees'

urlpatterns = [
    path('', views.FeesDashboardView.as_view(), name='dashboard'),
    path('structures/', views.FeeStructureListView.as_view(), name='fee_structure_list'),
    path('structure/create/', views.FeeStructureCreateView.as_view(), name='fee_structure_create'),
    path('student/<int:student_id>/fees/', views.StudentFeeListView.as_view(), name='student_fees'),
    path('payments/', views.PaymentListView.as_view(), name='payment_list'),
    path('payment/create/', views.PaymentCreateView.as_view(), name='payment_create'),
    path('payment/<int:pk>/', views.PaymentDetailView.as_view(), name='payment_detail'),
]
