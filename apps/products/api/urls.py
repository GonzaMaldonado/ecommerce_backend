from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from .views.general_views import MeasureUnitViewSet, CategoryProductViewSet, IndicatorViewSet
from .views.product_views import ProductViewSet

router = DefaultRouter()
# si agrego algo en r'' va a incluirse en el path de todas las ruta de ProductViewSet
router.register(r'product', ProductViewSet, basename='product')
router.register(r'category_product', CategoryProductViewSet, basename='category_product')
router.register(r'measure_unit', MeasureUnitViewSet, basename='measure_unit')
router.register(r'indicator', IndicatorViewSet, basename='indicator')

urlpatterns = [
    path('', include(router.urls), name='products'),
    path('docs/', include_docs_urls(title='Docs Product API')),
]