from django.contrib import admin

# Register your models here.
from .models.category import Category
from .models.products import Products
from .models.customer import Customer
from .models.orders import Order


class AdminProduct(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']

class CategoryProduct(admin.ModelAdmin):
    list_display = ['name']



admin.site.register(Products, AdminProduct)
admin.site.register(Category, CategoryProduct)
admin.site.register(Customer)
admin.site.register(Order)

