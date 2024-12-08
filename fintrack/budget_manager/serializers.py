from rest_framework import serializers
from .models import Budget
from transaction.serializers import UserSerializer, CategorySerializer
from transaction.models import Category, User

class BudgetSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Budget
        fields = ['id','category','limit']

    def create(self,validated_data):
        category_data = validated_data.pop('category')
        category = Category.objects.get(name=category_data['name'])
        
        validated_data.pop('user', None)

        budget = Budget.objects.create(
            category = category,
            user = self.context['request'].user,
            **validated_data
        )
        return budget
    
    def update(self, instance, validated_data):
        category_data = validated_data.pop('category', None)
        

        if category_data:
            category = Category.objects.get(name=category_data['name'])
            instance.category = category
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance