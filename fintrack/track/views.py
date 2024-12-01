from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from .models import *
#from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import json, logging
from django.utils import timezone


logger = logging.getLogger(__name__)
# Create your views here.
def create_transaction(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = get_object_or_404(request.user)
            transaction_type = get_object_or_404(TransactionType, id=data['id'])
            category = get_object_or_404(Category, id=data['category_id'])

            transaction = Transaction.objects.create(
                date = timezone.now(),
                type = transaction_type,
                category = category,
                amount = data['amount'],
                description = data['description'],
                user_id = user
            )
            logger.error(f"Error occurred: {str(e)}")
            response_data = {'message': 'Transaction created successfully', 'id': transaction.id}
            return Response(json.dumps(response_data), content_type="application/json", status=201)
        
        except Exception as e:
            response_data = {'message': str(e)}
            return Response(json.dumps(response_data), content_type="application/json", status=400)
        return Response(json.dumps({'error':'Invalid Http Method'}), content_type="application/json", status=405)

def update_transaction(request, transaction_id):
    if request.method == "PUT":
        try:
            data = json.loads(request.body) 
            transaction = get_object_or_404(Transaction, id=id)
            transaction.date = data.get('date', transaction.date)
            transaction.type = get_object_or_404(TransactionType, id=data.get['type_id']) if 'type_id' in data else transaction.type
            transaction.category = get_object_or_404(Category, id=data.get ['category_id']) if 'category_id' in data else transaction.category
            transaction.amount = data.get('amount', transaction.amount)
            transaction.description = data.get('description', transaction.description)
            transaction.save()
            response_data = {'message': 'Transaction updated successfully'}
            return Response(json.dumps(response_data), content_type="application/json", status=200)
        except Exception as e:
            response_data = {'message': str(e)}
            return Response(json.dumps(response_data), content_type="application/json", status=400)
        return Response(json.dumps({'error':'Invalid Http Method'}), content_type="application/json", status=405)


def delete_transaction(request, transaction_id):
    if request.method == 'DELETE':
        try:
            transaction = get_object_or_404(Transaction, id=transaction_id)
            transaction.delete
            response_data = {'message': 'Transaction deleted successfully'}
            return Response(json.dumps(response_data), content_type="application/json", status=200)
        except Exception as e:
            response_data = {'message': str(e)}
            return Response(json.dumps(response_data), content_type="application/json", status=400)
        return Response(json.dumps({'error':'Invalid Http Method'}), content_type="application/json", status=405)

