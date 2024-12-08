import random
from datetime import timedelta
from django.utils import timezone
from celery import shared_task
from .models import Transaction, TransactionType, Category, User, PaymentMethod

@shared_task
def generate_random_transactions():

    transaction_types = TransactionType.objects.all()
    categories = Category.objects.all()
    payment_methods = PaymentMethod.objects.all()
    users = User.objects.all()

    for user in users:
        transactions = random.randint(1,20)

        for _ in range(transactions):
            transaction_type = random.choice(transaction_types)
            category = random.choice(categories)
            payment_method = random.choice(payment_methods)
            amount = round(random.uniform(1.0, 1000.0), 2)
            description = category

            transaction = Transaction(
                date=timezone.now().date() - timedelta(days=random.randint(0, 30)),  # Random date within the last 30 days
                transaction_type=transaction_type,
                category=category,
                amount=amount,
                description=description,
                user=user,
                payment=payment_method
            )
            transaction.save() 