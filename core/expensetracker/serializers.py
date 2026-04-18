from rest_framework import serializers
from .models import User, Category, Expense


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class CategorySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'user', 'name', 'description', 'created_at']
        read_only_fields = ['id', 'created_at', 'user']


class ExpenseSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = Expense
        fields = ['id', 'user', 'category', 'category_id', 'amount', 'description', 'date', 'created_at']
        read_only_fields = ['id', 'created_at', 'user']
