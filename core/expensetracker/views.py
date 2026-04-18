from django.shortcuts import render

from django.http import HttpResponse
from rest_framework import generics, permissions
from .models import Category
from .serilizer import CategorySerializer   

# Create your views here.


class CategoryListView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)
       


def home(request):
    return HttpResponse("Welcome to the Expense Tracker API!")
    