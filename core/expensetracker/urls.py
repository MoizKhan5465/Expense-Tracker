
from django.urls import path,include
from expensetracker.views import home

urlpatterns = [

    path('', view=home, name='home'),
]
