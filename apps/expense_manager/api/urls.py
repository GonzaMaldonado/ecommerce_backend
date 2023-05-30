from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.expense_views import ExpenseViewSet

router = DefaultRouter()
router.register(r'expense', ExpenseViewSet, basename='expense')

urlpatterns = [
    path('', include(router.urls))
]