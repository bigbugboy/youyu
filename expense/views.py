from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
import datetime
import calendar
from collections import defaultdict


from .models import Category, Expense


@login_required(login_url='login')
def index(request):
    page = request.GET.get('page', 1)
    search = request.GET.get('search', '').strip()
    if not search:
        expenses = Expense.objects.all()
        for e in expenses:
            print(e.date)
    else:
        expenses = Expense.objects.filter(
            Q(owner=request.user),
            Q(amount__startswith=search)|
            Q(date__startswith=search)|
            Q(description__icontains=search)|
            Q(category__icontains=search)
        )

    paginator = Paginator(expenses, 3)
    context = {
        'page_obj': paginator.get_page(page),
        'search_text': search
    }
    
    return render(request, 'expense/index.html', context)


@login_required(login_url='login')
def add_expense(request):
    context = {
        'categories': Category.objects.all(),
        'values': request.POST,
    }
    if request.method == 'GET':
        return render(request, 'expense/add_expense.html', context)
    else:
        amount = request.POST['amount']
        category = request.POST['category']
        if not amount:
            messages.error(request, '数量不能为空')
            return render(request, 'expense/add_expense.html', context)
        if not category:
            messages.error(request, '类型不能为空')
            return render(request, 'expense/add_expense.html', context)
        
        Expense.objects.create(
            amount=amount,
            description=request.POST['description'],
            category=request.POST['category'],
            owner=request.user,
            date=request.POST['date']
        )
        messages.success(request, '添加成功')
        return redirect(to='expense')



@login_required(login_url='login')
def edit_expense(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense': expense,
        'values': expense,
        'categories': categories
    }
    if request.method == 'GET':
        return render(request, 'expense/edit_expense.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        category = request.POST['category']
        if not amount:
            messages.error(request, '数量不能为空')
            return render(request, 'expense/edit_expense.html', context)
        if not category:
            messages.error(request, '类型不能为空')
            return render(request, 'expense/edit_expense.html', context)
        
        expense.amount = amount
        expense.category = category
        expense.description = request.POST['description']
        date = request.POST['date']
        if date:
            expense.date = date
        expense.save()
        messages.success(request, '修改成功')
        return redirect(to='expense')


@login_required(login_url='login')
def delete_expense(request, id):
    Expense.objects.filter(pk=id).delete()
    messages.success(request, '删除成功')
    return redirect(to='expense')



@login_required(login_url='login')
def this_month_data_stats(request):
    start_date = datetime.date.today().replace(day=1)
    end_date = start_date.replace(
        day=calendar.monthrange(start_date.year, start_date.month)[1]
    )
    expenses = Expense.objects.filter(
        owner=request.user, 
        date__range=(start_date, end_date)
    ).all()

    # amount per category
    # amount per day
    category_dict = defaultdict(int)
    day_dict = defaultdict(int)
    for item in expenses:
        category_dict[item.category] += item.amount
        day_dict[item.date.day] += item.amount
    category_stats = [{'name': k, 'value': v} for k, v in category_dict.items()]
    day_stats = [[str(k), v] for k, v in day_dict.items()]


    response_data = {
        'category_stats': category_stats,
        'day_stats': sorted(day_stats, key=lambda x: x[0]),
    }
    return JsonResponse(response_data)


"""
[
        ['product', '2012', '2013', '2014', '2015', '2016', '2017'],
        ['Milk Tea', 56.5, 82.1, 88.7, 70.1, 53.4, 85.1],
        ['Matcha Latte', 51.1, 51.4, 55.1, 53.3, 73.8, 68.7],
        ['Cheese Cocoa', 40.1, 62.2, 69.5, 36.4, 45.2, 32.5],
        ['Walnut Brownie', 25.2, 37.1, 41.2, 18, 33.9, 49.1]
      ]
"""

@login_required(login_url='login')
def year_category_stats(request, year):
    start_day = datetime.date(year=year, month=1, day=1)
    end_day = datetime.date(year=year, month=12, day=31)

    expenses = Expense.objects.filter(owner=request.user, date__range=(start_day, end_day)).all()
    categories = Category.objects.all()
    stats = {c.name: [0 for _ in range(12)] for c in categories}
    for item in expenses:
        category = item.category
        month = item.date.month
        stats[category][month - 1] += item.amount
    
    response_data = [[k] + v for k, v in stats.items()]
    response_data.insert(0, ['product'] + [str(i + 1) for i in range(12)])

    return JsonResponse({
        'response_data': response_data
    })



@login_required(login_url='login')
def expense_summary_index(request):
    today = datetime.date.today() 
    start_date = today.replace(year=today.year - 1, month=1, day=1)
    
    today_sum_stats = {'title': '今天', 'count': 0, 'sum': 0}
    this_month_sum_stats = {'title': '本月', 'count': 0, 'sum': 0}
    this_year_sum_stats = {'title': '今年', 'count': 0, 'sum': 0}
    last_yesr_sum_stats = {'title': '去年', 'count': 0, 'sum': 0}
    expenses = Expense.objects.filter(owner=request.user, date__gte=start_date).all()
    for item in expenses:
        if item.date == today:
            today_sum_stats['count'] += 1
            today_sum_stats['sum'] += item.amount
        if item.date >= today.replace(day=1):
            this_month_sum_stats['count'] += 1
            this_month_sum_stats['sum'] += item.amount
        if item.date >= today.replace(month=1, day=1):
            this_year_sum_stats['count'] += 1
            this_year_sum_stats['sum'] += item.amount
        else:
            last_yesr_sum_stats['count'] += 1
            last_yesr_sum_stats['sum'] += item.amount


    context = {
        'sum_stats_list': [
            today_sum_stats, this_month_sum_stats, this_year_sum_stats,last_yesr_sum_stats
        ],
    }

    return render(request, 'expense/summary_index.html', context)