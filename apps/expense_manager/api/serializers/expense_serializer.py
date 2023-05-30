from rest_framework import serializers
from apps.expense_manager.models import Expense, Supplier


class SupplierRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        exclude = ('state', 'created', 'updated', 'deleted')
        

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        exclude = ('state', 'created', 'updated', 'deleted')