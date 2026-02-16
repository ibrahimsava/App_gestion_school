from django.urls import path
from . import views

app_name = 'librairy'

urlpatterns = [
    path('', views.LibraryDashboardView.as_view(), name='dashboard'),
    path('books/', views.BookListView.as_view(), name='book_list'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('book/add/', views.BookCreateView.as_view(), name='book_create'),
    path('issue/<int:pk>/', views.BookIssueDetailView.as_view(), name='issue_detail'),
    path('issue/create/', views.BookIssueCreateView.as_view(), name='issue_create'),
    path('issue/<int:pk>/return/', views.BookReturnCreateView.as_view(), name='return_create'),
    path('my-books/', views.MyBooksView.as_view(), name='my_books'),
]
