from django.contrib import admin
from .models import Supplier, Voucher, PaymentType, Expense, ExpenseCategory, Merma

admin.site.register(Supplier)
admin.site.register(PaymentType)
admin.site.register(Voucher)
admin.site.register(ExpenseCategory)
admin.site.register(Expense)
admin.site.register(Merma)