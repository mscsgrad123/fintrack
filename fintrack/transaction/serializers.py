from rest_framework import serializers
from .models import User, Transaction, TransactionType, Category, PaymentMethod

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

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ['id','name','description']

class TransactionSerializer(serializers.ModelSerializer):
    transaction_type = TransactionTypeSerializer()
    category = CategorySerializer()
    payment = PaymentMethodSerializer()

    class Meta:
        model=Transaction
        fields=['id','date','transaction_type','category','amount','description','payment']

    def create(self,validated_data):
        transaction_type_data = validated_data.pop('transaction_type')
        category_data = validated_data.pop('category')
        payment_data = validated_data.pop('payment')

        transaction_type = TransactionType.objects.get(name=transaction_type_data['name'])
        category = Category.objects.get(name=category_data['name'])
        payment = PaymentMethod.objects.get(name=payment_data['name'])

        validated_data.pop('user',None)

        transaction = Transaction.objects.create(
            transaction_type=transaction_type,
            category = category,
            payment = payment,
            user = self.context['request'].user,
            **validated_data
        )

        return transaction
    
    def update(self,instance,validated_data):
        transaction_type_data = validated_data.pop('transaction_type', None)
        category_data = validated_data.pop('category', None)
        payment_data = validated_data.pop('payment', None)

        if transaction_type_data:
            transaction_type = TransactionType.objects.get(name=transaction_type_data['name'])
            instance.transaction_type = transaction_type
        if category_data:
            category = Category.objects.get(name=category_data['name'])
            instance.category = category
        if payment_data:
            payment = PaymentMethod.objects.get(name=payment_data['name'])
            instance.payment = payment

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance