from rest_framework import serializers
from expensetracker.models import User, Category, Expense
from django.db import models

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CategorySerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d %b %Y, %I:%M %p", read_only=True)
    user=serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Category
        fields = ['id','user','email', 'name', 'created_at', 'description']
        read_only_fields = ['created_at','id']

class ExpenseSerializer(serializers.ModelSerializer):
    user=serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        required=False,
        allow_null=True
    )
    
    category_name=serializers.CharField(source='category.name', read_only=True, default=None)
    description=serializers.CharField(source='category.description', read_only=True)
    created_at_for_catogory=serializers.DateTimeField(source='category.created_at', format="%d %b %Y, %I:%M %p", read_only=True)
    
    created_at = serializers.DateTimeField(format="%d %b %Y, %I:%M %p", read_only=True)
    

    class Meta:
        model = Expense
        fields = ['id','user','email', 'amount', 'date', 'created_at','user','category','category_name','description','created_at_for_catogory']

    def validate_amount(self,value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value
    


class SummarySerializer(serializers.ModelSerializer):
    user=serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    category=serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Expense
        fields = ['user','email', 'category']