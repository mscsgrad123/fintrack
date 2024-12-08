from rest_framework import serializers
from .models import User, Transaction, TransactionType, Category

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','name','email','password']

class TransactionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=TransactionType
        fields=['id','name','description']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','name','description']

class TransactionSerializer(serializers.ModelSerializer):
    transaction_type = TransactionTypeSerializer()
    category = CategorySerializer()

    class Meta:
        model=Transaction
        fields=['id','date','transaction_type','category','amount','description']

    def create(self,validated_data):
        transaction_type_data = validated_data.pop('transaction_type')
        category_data = validated_data.pop('category')

        transaction_type = TransactionType.objects.get(name=transaction_type_data['name'])
        category = Category.objects.get(name=category_data['name'])

        validated_data.pop('user',None)

        transaction = Transaction.objects.create(
            transaction_type=transaction_type,
            category = category,
            user = self.context['request'].user,
            **validated_data
        )

        return transaction
    
    def update(self,instance,validated_data):
        transaction_type_data = validated_data.pop('transaction_type', None)
        category_data = validated_data.pop('category', None)

        if transaction_type_data:
            transaction_type = TransactionType.objects.get(name=transaction_type_data['name'])
            instance.transaction_type = transaction_type
        if category_data:
            category = Category.objects.get(name=category_data['name'])
            instance.category = category
        

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance