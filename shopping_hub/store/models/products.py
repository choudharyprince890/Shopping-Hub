from django.db import models

from .category import Category
# Create your models here.

class Products(models.Model):
    filename = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    size = models.CharField(max_length=10,null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=200, default='', blank=True, null=True)
    image_url = models.URLField(null=True, blank=True)
    image = models.ImageField(upload_to='uploads/products/', null=True, blank=True)


    def __str__(self):
        return self.name
