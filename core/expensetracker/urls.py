
from django.urls import path,include
from expensetracker.views import home
from expensetracker.views import CategoryListView

urlpatterns = [

    path('', view=home, name='home'),
    path('categories/', view=CategoryListView.as_view(), name='category-list'),
]
