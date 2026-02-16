from django.db import models

# Create your models here.

# ==================== LIBRARY APP ====================

class Book(models.Model):
    """Book model"""
    BOOK_STATUS = (
        ('available', 'Available'),
        ('issued', 'Issued'),
        ('damaged', 'Damaged'),
        ('lost', 'Lost'),
    )
    
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=20, unique=True)
    publisher = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    category = models.CharField(max_length=100)
    quantity = models.IntegerField()
    available_quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=BOOK_STATUS, default='available')
    book_shelf = models.CharField(max_length=50, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    added_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Books'
    
    def __str__(self):
        return f"{self.title} by {self.author}"


class BookIssue(models.Model):
    """Book Issue model"""
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='issues')
    student = models.ForeignKey('account.Student', on_delete=models.CASCADE, related_name='book_issues')
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    issued_by = models.ForeignKey('account.User', on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)
    remarks = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = 'Book Issues'
        ordering = ['-issue_date']
    
    def __str__(self):
        return f"{self.book.title} - {self.student.user.get_full_name()}"


class BookReturn(models.Model):
    """Book Return model"""
    book_issue = models.OneToOneField(BookIssue, on_delete=models.CASCADE, related_name='book_return')
    return_date = models.DateField()
    book_condition = models.CharField(
        max_length=20,
        choices=(('good', 'Good'), ('fair', 'Fair'), ('damaged', 'Damaged')),
        default='good'
    )
    returned_by = models.ForeignKey('account.User', on_delete=models.SET_NULL, null=True)
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    remarks = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = 'Book Returns'
    
    def __str__(self):
        return f"Return: {self.book_issue.book.title} on {self.return_date}"
