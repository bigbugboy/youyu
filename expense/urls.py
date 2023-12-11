from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='expense'),
    path('add-expense', views.add_expense, name='add-expense'),
    path('edit-expense/<id>', views.edit_expense, name='edit-expense'),
    path('delete-expense/<id>', views.delete_expense, name='delete-expense'),
    path('download_csv', views.download_csv),
    path('download_pdf', views.download_pdf),
    path('download_excel', views.download_excel),
    path('index_stats', views.index_stats, name='index_stats'),
    # summary page
    path('expense-summary', views.expense_summary, name='expense-summary'),
    path('expense-s1', views.expense_s1, name='expense-s1'),
    path('expense-s2', views.expense_s2, name='expense-s2'),
    path('expense-s3', views.expense_s3, name='expense-s3'),
    path('expense-s4/<int:year>', views.expense_s4, name='expense-s4'),
    
]