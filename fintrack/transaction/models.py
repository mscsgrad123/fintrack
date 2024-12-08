from django.db import models
import datetime
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50,unique=True,default='default_username')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    # REQUIRED_FIELDS= ['email', 'password']
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

class TransactionType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description=models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class PaymentMethod(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def _str_(self):
        return self.name

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name

class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(default=datetime.date.today)
    transaction_type = models.ForeignKey(TransactionType,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE) 


    def __str__(self):
        return self.description
    


    
