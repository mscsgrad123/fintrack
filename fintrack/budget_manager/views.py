from rest_framework import viewsets,status
from rest_framework.response import Response
from .models import Budget
from .serializers import BudgetSerializer
from django.db.models import Sum
from transaction.models import Transaction
from rest_framework.pagination import PageNumberPagination


class BudgetPagination(PageNumberPagination):
    page_size=5
    page_size_query_param='page_size'
    max_page_size=30


class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)
    
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)

    def perform_update(self,serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """Override create to validate if budget already exists for a category."""
        user = request.user
        category_id = request.data.get('category')

        if Budget.objects.filter(user=user, category_id=category_id).exists():
            return Response(
                {"error": "Budget for this category already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().create(request, *args, **kwargs)
    

    def list(self, request, *args, **kwargs):
        
        """List budgets with additional expense status."""
        budgets = self.get_queryset()
        response_data = []


        for budget in budgets:
            # Calculate total expenses for this category
            total_expenses = Transaction.objects.filter(
                user=request.user, category=budget.category
            ).aggregate(total=Sum('amount'))['total'] or 0

            # Add budget details and status
            status_message = self.get_budget_status_message(total_expenses, budget.limit)
            response_data.append({
                "id": budget.id,
                "category": budget.category.name,
                "limit": budget.limit,
                "total_expenses": total_expenses,
                "status": status_message
            })

        pagination = self.pagination_class()
        paginated_response = pagination.paginate_queryset(response_data, request)
        return pagination.get_paginated_response(paginated_response)
    


    def get_budget_status_message(self, total_expenses, limit):
        percentage = (total_expenses / limit) * 100 if limit > 0 else 0
        if percentage > 100:
            return "Limit exceeded!"
        elif percentage==100:
            return "Limit reached!"
        elif percentage >= 90:
            return "90'%' of the limit reached!"
        
        
    def destroy(self, request, *args, **kwargs):
        """Override destroy to add custom logic for budget deletion."""
        budget = self.get_object()
        
        # You can add custom checks here if needed, e.g., if the user has permission to delete
        if budget.user != request.user:
            return Response(
                {"detail": "You do not have permission to delete this budget."},
                status=status.HTTP_403_FORBIDDEN
            )

        # If no custom logic needed, DRF's default behavior will handle deletion
        return super().destroy(request, *args, **kwargs)