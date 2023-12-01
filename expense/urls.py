from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='expense'),
    path('add-expense', views.add_expense, name='add-expense'),
    path('edit-expense/<id>', views.edit_expense, name='edit-expense'),
    path('delete-expense/<id>', views.delete_expense, name='delete-expense'),
    path('download_csv', views.doanload_csv),
    path('download_pdf', views.doanload_pdf),
    path('index_stats', views.index_stats, name='index_stats'),
    # summary
    path('expense-summary', views.expense_summary_index, name='expense_summary'),
    path('year_category_stats/<int:year>', views.year_category_stats, name='year_category_stats'),
    
]