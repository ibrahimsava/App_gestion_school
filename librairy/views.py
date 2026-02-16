from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Book, BookIssue, BookReturn
from account.models import Student

# ==================== LIBRARY DASHBOARD ====================

class LibraryDashboardView(LoginRequiredMixin, TemplateView):
    """Library dashboard"""
    template_name = 'librairy/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_books'] = Book.objects.count()
        context['available_books'] = Book.objects.filter(status='available').count()
        context['issued_books'] = BookIssue.objects.count()
        return context


# ==================== BOOK VIEWS ====================

class BookListView(LoginRequiredMixin, ListView):
    """List all books"""
    model = Book
    template_name = 'librairy/book_list.html'
    paginate_by = 20
    
    def get_queryset(self):
        return Book.objects.filter(status='available')


class BookDetailView(LoginRequiredMixin, DetailView):
    """Book detail view"""
    model = Book
    template_name = 'librairy/book_detail.html'


class BookCreateView(LoginRequiredMixin, CreateView):
    """Add new book"""
    model = Book
    template_name = 'librairy/book_form.html'
    fields = ['title', 'author', 'isbn', 'publisher', 'publication_year', 'category', 'quantity', 'available_quantity', 'book_shelf', 'price']
    success_url = reverse_lazy('librairy:book_list')


# ==================== BOOK ISSUE VIEWS ====================

class BookIssueDetailView(LoginRequiredMixin, DetailView):
    """Book issue detail view"""
    model = BookIssue
    template_name = 'librairy/issue_detail.html'


class BookIssueCreateView(LoginRequiredMixin, CreateView):
    """Issue a book to a student"""
    model = BookIssue
    template_name = 'librairy/issue_form.html'
    fields = ['book', 'student', 'due_date', 'quantity', 'remarks']
    success_url = reverse_lazy('librairy:book_list')
    
    def form_valid(self, form):
        form.instance.issued_by = self.request.user
        return super().form_valid(form)


# ==================== BOOK RETURN VIEWS ====================

class BookReturnCreateView(LoginRequiredMixin, CreateView):
    """Return an issued book"""
    model = BookReturn
    template_name = 'librairy/return_form.html'
    fields = ['return_date', 'book_condition', 'fine_amount', 'remarks']
    success_url = reverse_lazy('librairy:book_list')
    
    def get_object(self):
        return get_object_or_404(BookIssue, pk=self.kwargs.get('pk'))
    
    def form_valid(self, form):
        form.instance.returned_by = self.request.user
        form.instance.book_issue = self.get_object()
        return super().form_valid(form)


# ==================== MY BOOKS VIEW ====================

class MyBooksView(LoginRequiredMixin, ListView):
    """View books issued to the current user"""
    model = BookIssue
    template_name = 'librairy/my_books.html'
    paginate_by = 10
    
    def get_queryset(self):
        try:
            student = Student.objects.get(user=self.request.user)
            return BookIssue.objects.filter(student=student, book_return__isnull=True).select_related('book')
        except Student.DoesNotExist:
            return BookIssue.objects.none()
