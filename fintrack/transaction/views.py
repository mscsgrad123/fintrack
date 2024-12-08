from rest_framework import viewsets
from .models import Transaction,User,TransactionType,Category
from .serializers import TransactionSerializer,UserSerializer,TransactionTypeSerializer,CategorySerializer
from budget_manager.models import Budget
from django.db.models import Sum
from rest_framework.pagination import PageNumberPagination

class CommonPaginator(PageNumberPagination):
    page_size=5
    page_size_query_param='page_size'
    max_page_size=30


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    pagination_class = PageNumberPagination

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination

class TransactionTypeViewSet(viewsets.ModelViewSet):
    queryset = TransactionType.objects.all()
    serializer_class = TransactionTypeSerializer
    pagination_class = PageNumberPagination

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
