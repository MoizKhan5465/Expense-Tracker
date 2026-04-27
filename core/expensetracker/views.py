from django.shortcuts import render
from django.http import HttpResponse
from django.db import models
from rest_framework import generics, permissions
from .models import Category,Expense
from .serilizers import CategorySerializer  ,ExpenseSerializer,SummarySerializer
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import viewsets
from django.db.models import Sum, Count
from decimal import Decimal
# Create your views here.
from rest_framework.pagination import PageNumberPagination
from expensetracker.filters import ExpenseFilter
from django_filters.rest_framework import DjangoFilterBackend

class PagenumberPagiantion(PageNumberPagination):
    page_size = 10
    page_size_query_param='page_size'
    max_page_size=100
    


class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.none()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Schema generation or unauthenticated access
        if getattr(self, "swagger_fake_view", False) or not user.is_authenticated:
            return Category.objects.none()

        # Admin access
        if user.is_staff:
            return Category.objects.all()

        # User-specific data
        return Category.objects.filter(user=user)

class ExpenseListView(generics.ListCreateAPIView):
    queryset = Expense.objects.none()
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class=PagenumberPagiantion

    filter_backends = [DjangoFilterBackend]   # REQUIRED
    filterset_class = ExpenseFilter           # REQUIRED

    def get_queryset(self):
        User=self.request.user
        queryset = Expense.objects.select_related('user', 'category')
        if getattr(self, 'swagger_fake_view', False) or not User.is_authenticated:
            return queryset.none()
        
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
        if getattr(self, 'swagger_fake_view', False) or not User.is_authenticated:
            return queryset.none()
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
        if getattr(self, 'swagger_fake_view', False) or not User.is_authenticated:
            return queryset.none()
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
        if getattr(self, 'swagger_fake_view', False) or not User.is_authenticated:
             return queryset.none()
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
    