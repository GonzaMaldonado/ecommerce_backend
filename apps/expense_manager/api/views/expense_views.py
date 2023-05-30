from django.db.models import Q

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from apps.base.utils import format_date

from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.expense_manager.models import Supplier, Voucher, PaymentType
from apps.expense_manager.api.serializers.expense_serializer import (ExpenseSerializer,
                                                                     SupplierRegisterSerializer)
from apps.expense_manager.api.serializers.general_serializer import (SupplierSerializer,
                                                                     VoucherSerializer,
                                                                     PaymentTypeSerializer,
                                                                     ProductSerializer)
from apps.products.models import Product


class ExpenseViewSet(viewsets.GenericViewSet):
    serializer_class = ExpenseSerializer

    @action(methods=['get'], detail=False)
    def search_supplier(self, request):
        ruc_or_business_name = request.query_params.get('ruc_or_business_name', '')
        supplier = Supplier.objects.filter(
            Q(ruc__iexact=ruc_or_business_name) |
            Q(business_name__iexact=ruc_or_business_name)
        ).first()
        if supplier:
            supplier_serializer = SupplierSerializer(supplier)
            return Response(supplier_serializer.data)
        return Response({'error': 'No se ha encontrado un Proveedor'},status=status.HTTP_404_NOT_FOUND)


    @action(methods=['post'], detail=False)
    def new_supplier(self,request):
        supplier = SupplierRegisterSerializer(data=request.data)

        if supplier.is_valid():
            supplier.save()
            return Response({'message': 'Proveedor registrado correctamente',
                             'supplier': supplier.data},
                             status=status.HTTP_201_CREATED)
        return Response({'message': 'Datos de Proveedor invalidos',
                        'error': supplier.errors},
                        status=status.HTTP_400_BAD_REQUEST)
        

    @action(methods=['get'], detail=False)
    def get_vouchers(self, request):
        voucher = Voucher.objects.filter(state=True).order_by('id')
        voucher = VoucherSerializer(voucher, many=True)
        return Response(voucher.data)
    

    @action(methods=['get'], detail=False)
    def get_payment_types(self, request):
        payment_type = PaymentType.objects.filter(state=True).order_by('id')
        payment_type = PaymentTypeSerializer(payment_type, many=True)
        return Response(payment_type.data)
    

    @action(methods=['get'], detail=False)
    def get_products(self, request):
        product = Product.objects.filter(state=True).order_by('id')
        product = ProductSerializer(product, many=True)
        return Response(product.data)
        

    def create(self, request):
        expense = request.data
        JWT_authenticator = JWTAuthentication()
        # Decode token - retorn el usuario y el token
        user, _ = JWT_authenticator.authenticate(request)
        expense['user'] = user.id
        # Formateando la fecha recibida de dd/mm/YY a YY/mm/dd
        print(expense['date'])
        expense['date'] = format_date(expense['date'])
        expense_serializer = ExpenseSerializer(data=expense)

        if expense_serializer.is_valid():
            expense_serializer.save()
            return Response({'message': 'Factura registrada correctamente',
                             'expense': expense_serializer.data},
                             status=status.HTTP_201_CREATED)
        return Response({'message': 'Han ocurrido errores en la creación.',
                         'error': expense_serializer.errors},
                         status=status.HTTP_400_BAD_REQUEST)