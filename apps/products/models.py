from django.db import models
from apps.base.models import BaseModel


class MeasureUnit(BaseModel):
    description = models.CharField(max_length=50, unique=True)

        
    def __str__(self):
        return self.description



class CategoryProduct(BaseModel):
    description = models.CharField(max_length=100, unique=True)

        
    def __str__(self):
        return self.description



class Indicator(BaseModel):
    descount_value = models.PositiveSmallIntegerField(default=0)
    category_product = models.ForeignKey(CategoryProduct, on_delete=models.CASCADE)

        
    def __str__(self):
        return f'{self.category_id} : {self.descount_value}'



class Product(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=255)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    measure_unit = models.ForeignKey(MeasureUnit, on_delete=models.CASCADE, null=True)
    category_product = models.ForeignKey(CategoryProduct, on_delete=models.CASCADE, null=True)

        
    def __str__(self):
        return self.name
    