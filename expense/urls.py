from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='expense'),
    path('add-expense', views.add_expense, name='add-expense'),
    path('edit-expense/<id>', views.edit_expense, name='edit-expense'),
    path('delete-expense/<id>', views.delete_expense, name='delete-expense'),
    path('expense-summary', views.expense_summary_index, name='expense_summary'),
    path('this_month_data_stats', views.this_month_data_stats, name='this_month_data_stats'),
    path('year_category_stats/<int:year>', views.year_category_stats, name='year_category_stats'),
]