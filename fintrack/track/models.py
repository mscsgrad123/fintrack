from django.db import models

# Create your models here.

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField()

class TransactionType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description=models.CharField(max_length=100)

class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    type = models.ForeignKey(TransactionType,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=100)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)    



