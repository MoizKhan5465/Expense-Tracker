from expensetracker.models import Expense
import django_filters

class ExpenseFilter(django_filters.FilterSet):
    user=django_filters.CharFilter(field_name='user__username', lookup_expr='iexact')
    category=django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    min_amount=django_filters.NumberFilter(field_name='amount', lookup_expr='gte')
    max_amount=django_filters.NumberFilter(field_name='amount', lookup_expr='lte')
    start_date=django_filters.DateFilter(field_name='date', lookup_expr='gte')
    end_date=django_filters.DateFilter(field_name='date', lookup_expr='lte')


    class Meta:
        model=Expense
        fields=['user','category','min_amount','max_amount','start_date','end_date']