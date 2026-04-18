from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass


class Category(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,related_name="categories")
    name=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_category_per_user')
        ]

    
    def __str__(self):
        return self.name



class Expense(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,related_name="expenses")
    category=models.ForeignKey('Category', on_delete=models.SET_NULL, null=True,blank =True,related_name="expenses")
    
    amount=models.DecimalField(max_digits=10, decimal_places=2)
    description=models.CharField(max_length=255, blank=True)
    date=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount} - {self.user.username}"

    




