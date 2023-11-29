from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def index(request):
    print(request.user)
    return render(request, 'expense/index.html')
