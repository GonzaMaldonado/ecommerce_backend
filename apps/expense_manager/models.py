from django.db import models

from apps.base.models import BaseModel
from apps.products.models import Product


class Supplier(BaseModel):
    ruc = models.CharField(unique=True, max_length=11)
    business_name = models.CharField(max_length=150)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.business_name

class PaymentType(BaseModel):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name

    
class Voucher(BaseModel):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class ExpenseCategory(BaseModel):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name
    

class Expense(BaseModel):
    date = models.DateField(auto_now=False, auto_now_add=False)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    voucher_number = models.CharField(max_length=50)
    total = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.voucher_number
    

class Merma(BaseModel):
    date = models.DateField(auto_now=False, auto_now_add=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=7, decimal_places=2)
    lost_money = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'Merma de {self.product.__str__}'