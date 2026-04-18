from rest_framework import serializers
from expensetracker.models import User, Category, Expense

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at']
        read_only_fields = ['created_at']

class ExpenseSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        required=False,
        allow_null=True
    )
    category_detail=CategorySerializer(source='category', read_only=True)

    class Meta:
        model = Expense
        fields = ['id', 'amount', 'description', 'date', 'created_at','user','category','category_detail']

    def validate_amount(self,value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value
    
    def validate_category(self, value):
        request = self.context.get('request')
        if value and value.user != request.user:
            raise serializers.ValidationError("Invalid category")
        return value