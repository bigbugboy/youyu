from django.db import models
from django.contrib.auth.models import User


class Expense(models.Model):
    amount = models.FloatField(null=False)
    date = models.DateField(null=False)   # 慎用auto_now_add,导致时间无法自定义
    description = models.TextField(default='')
    category = models.CharField(max_length=255, null=False)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.category
        
    class Meta:
        ordering = ['-date']


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self) -> str:
        return self.name