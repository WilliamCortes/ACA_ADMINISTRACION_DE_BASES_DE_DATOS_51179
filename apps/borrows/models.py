from django.db import models


class Borrow(models.Model):
    STATUS_CHOICES = [
        ('BORROWED', 'Borrowed'),
        ('RETURNED', 'Returned'),
        ('LATE', 'Late'),
    ]

    borrow_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='borrows'
    )
    book = models.ForeignKey(
        'books.Book',
        on_delete=models.CASCADE,
        related_name='borrows'
    )
    borrow_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='BORROWED'
    )

    class Meta:
        db_table = 'borrows'

    def __str__(self):
        return f"Borrow #{self.borrow_id} — {self.user} / {self.book}"
