from django.contrib import admin
from .models import Book, BookIssue, BookReturn

# ==================== LIBRARY ADMIN ====================

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'quantity', 'available_quantity', 'status', 'category']
    search_fields = ['title', 'author', 'isbn']
    list_filter = ['status', 'category', 'publication_year']
    readonly_fields = ['added_date']


@admin.register(BookIssue)
class BookIssueAdmin(admin.ModelAdmin):
    list_display = ['book', 'student', 'issue_date', 'due_date', 'issued_by', 'quantity']
    search_fields = ['book__title', 'student__user__username']
    list_filter = ['issue_date', 'due_date']
    readonly_fields = ['issue_date']
    ordering = ['-issue_date']


@admin.register(BookReturn)
class BookReturnAdmin(admin.ModelAdmin):
    list_display = ['book_issue', 'return_date', 'book_condition', 'fine_amount', 'returned_by']
    search_fields = ['book_issue__book__title', 'book_issue__student__user__username']
    list_filter = ['book_condition', 'return_date']
