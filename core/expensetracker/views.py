from django.shortcuts import render
from django.http import HttpResponse
from django.db import models
from rest_framework import generics, permissions
from .models import Category,Expense
from .serilizer import CategorySerializer  ,ExpenseSerializer,SummarySerializer
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import viewsets
from django.db.models import Sum, Count
from decimal import Decimal
# Create your views here.


class CategoryListView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        User=self.request.user
        if User.is_staff:
             return Category.objects.all()
        return Category.objects.filter(user=User)

class ExpenseListView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        User=self.request.user
        queryset = Expense.objects.select_related('user', 'category')
        if User.is_staff:
             return queryset
        return queryset.filter(user=User)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class category_create_edit_delete_update(viewsets.ModelViewSet):
    queryset=Category.objects.select_related('user')
    serializer_class=CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        User=self.request.user
        queryset=super().get_queryset()
        if User.is_staff:
             return queryset
        return queryset.filter(user=User)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class Expense_create_edit_delete_update(viewsets.ModelViewSet):
    queryset = Expense.objects.select_related('user', 'category')
    serializer_class=ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        User=self.request.user
        queryset=super().get_queryset()
        if User.is_staff:
             return queryset
        return queryset.filter(user=User)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class ExpenseSummaryView(generics.ListAPIView):
    queryset = Expense.objects.select_related('user', 'category')
    serializer_class=SummarySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        User=self.request.user
        queryset=super().get_queryset()
        return queryset.filter(user=User)
    
    
    def category_breakdown(self,queryset):
        data= (
            queryset
            .values(category__name=models.F('category__name'))
            .annotate(total=Sum('amount'))
            .order_by('-total')
        )

        
        return [
        {"category": item["category__name"], "total": item["total"]}
        for item in data
    ]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        breakdown = self.category_breakdown(queryset)
        total = queryset.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        total_distinct_categories=queryset .exclude(category__isnull=True).values('category').distinct().count() or 0
        return Response({
            'total_expense': str(total),
            'breakdown ': breakdown,
            'total_categories': total_distinct_categories
        })
    