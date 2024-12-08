from django.db import models
from transaction.models import User, Category

# Create your models here.

class Budget(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    limit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.name} - {self.category.name} - {self.limit}"
    