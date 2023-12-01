from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse, FileResponse
from reportlab.pdfgen import canvas

from io import BytesIO
import csv
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
        context['values'] = request.POST
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
    return HttpResponse('ok') 


@login_required(login_url='login')
def doanload_csv(request):
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="expense.csv"'},
    )
    writer = csv.writer(response)
    writer.writerow(["金额", "类型", "日期", "描述"])
    for item in Expense.objects.filter(owner=request.user).all():
        row = [item.amount, item.category, str(item.date), item.description]
        writer.writerow(row)

    return response


@login_required(login_url='login')
def doanload_pdf(request):
    bio = BytesIO()
    pdf = canvas.Canvas(bio)
    pdf.drawString(100, 100, 'hello world')
    pdf.showPage()
    pdf.save()
    bio.seek(0)     # 一定要移动到0，否则没有数据
    return FileResponse(bio, as_attachment=True, filename="expense.pdf")


@login_required(login_url='login')
def index_stats(request):
    # 本月数据统计【用于支出页面的统计展示需求】
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
    
    day_list = sorted(day_dict.keys(), key=lambda x: x)
    response_data = {
        'category': [{'name': k, 'value': v} for k, v in category_dict.items()],
        'daily': {
            'keys': day_list,
            'values': [day_dict[k] for k in day_list]
        }
    }
    return JsonResponse(response_data)


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