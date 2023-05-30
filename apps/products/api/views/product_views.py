from rest_framework import viewsets, status
from rest_framework.response import Response
from apps.products.api.serializers.product_serializer import ProductSerializer

from apps.base.utils import validate_files


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state=True)
        return self.get_serializer().Meta.model.objects.filter(id=pk, state=True).first()
    

    def create(self, request, *args, **kwargs):
        data = validate_files(request.data, 'image')
        # Obteniendo el serializador de Product
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def update(self, request, *args, **kwargs):
        if self.get_queryset(kwargs['pk']):
            data = validate_files(request.data, 'image', True)
            product_serializer = self.serializer_class(self.get_queryset(kwargs['pk']), data=data)
            if product_serializer.is_valid():
                product_serializer.save()
                return Response(product_serializer.data)
            return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'No existe un producto con estos datos'}, status=status.HTTP_404_NOT_FOUND)
    

    #Con este método estoy haciendo eliminacion lógica, si no lo hago se elimina de la BBDD
    #Superpongo el método delete para que solo cambiando su state=False, asi no aparezca en las consultas
    def destroy(self, request, *args, **kwargs):
        product = self.get_queryset(kwargs['pk'])
        if product:
            product.state = False
            product.save()
            return Response({'detail':'Producto eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'errors':'No existe un producto con estos datos'}, status=status.HTTP_400_BAD_REQUEST)
