from django.db import models
# from manager.models import Book
from accounts.models import User


class Borrower(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    book_isbn = models.ForeignKey('manager.Book', on_delete=models.CASCADE,default='0')
    borrowed_from_date = models.DateTimeField(auto_now_add=True)
    borrowed_to_date =  models.DateTimeField()
    actual_return_date = models.DateTimeField(null=True)
    issued_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='book_issued_by')
    

class Payments(models.Model):
    payment_id = models.IntegerField(auto_created=True)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    book_isbn = models.ForeignKey('manager.Book', on_delete=models.CASCADE,default='0')
    late_fees_charged = models.CharField(max_length=50)
    payment_url = models.URLField(null=True,blank=True)
    payment_status = models.BooleanField(default=False)
    payment_date = models.DateTimeField(auto_now_add=True)

