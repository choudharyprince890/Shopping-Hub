from django.db import models

# Create your models here.

class trialProducts(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    size = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='uploads/trialproducts/', null=True, blank=True)


    def __str__(self):
        return self.name
