
from django.urls import path,include

from expensetracker.views import CategoryListView,ExpenseListView,category_create_edit_delete_update
from rest_framework.routers import DefaultRouter
from . import views
urlpatterns = [

    path('', view=ExpenseListView.as_view(), name='Expense-list'),
    path('categories/', view=CategoryListView.as_view(), name='category-list'),
    path('summary/', view=views.ExpenseSummaryView.as_view(), name='expense-summary'),
    
    
]


router=DefaultRouter()
router.register('create_category', views.category_create_edit_delete_update, basename='create_category')
router.register('create_expense', views.Expense_create_edit_delete_update, basename='create_expense')
urlpatterns += router.urls