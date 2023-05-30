from apps.base.api import GeneralListAPIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from apps.products.api.serializers.general_serializer import MeasureUnitSerializer, CategoryProductSerializer, IndicatorSerializer


class MeasureUnitViewSet(viewsets.GenericViewSet, GeneralListAPIView):
    serializer_class = MeasureUnitSerializer

    def get_object(self):
        return self.get_serializer().Meta.model.objects.filter(id=self.kwargs['pk'], state=True)
    

    def list(self, request):
        """
        Retorna todas las unidades de medida

        data
        description --- Nombre de la unidad de medida 
        """
        data = self.get_queryset()
        data = self.get_serializer(data, many=True)
        return Response(data.data)
    

    def create(self,request):
        """
        Crear una unidad de medida

        data
        description --- Nombre de la unidad de medida 
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Unidad de medida registrada correctamente'},status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    

    def update(self, request, *args, **kwargs):
        """
        Crear una unidad de medida

        data
        id --- Identificador de la unidad
        description --- Nombre de la unidad de medida 
        """
        if self.get_object().exists():
            serializer = self.serializer_class(instance=self.get_object().get(), data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message':'Unidad de medida actualizada correctamente'},status=status.HTTP_200_OK)
        return Response({'error': 'Unidad de medida no encontrada'},status=status.HTTP_404_NOT_FOUND)


    def destroy(self, request, *args, **kwargs):
        """
        Elimina una unidad de medida

        data
        id --- Identificador de la unidad
        description --- Nombre de la unidad de medida 
        """
        if self.get_object().exists():
            #Eliminacion Directa de la BBDD
            #self.get_object().get().delete()
            #Eliminacion lógica
            self.get_object().get().state = False
            return Response({'message':'Unidad de medida eliminada correctamente'},status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Unidad de medida no encontrada'},status=status.HTTP_404_NOT_FOUND)
    


class CategoryProductViewSet(viewsets.GenericViewSet, GeneralListAPIView):
    serializer_class = CategoryProductSerializer
    

    def list(self, request):
        """
        Retorna todas las categorias

        params.
        description --- Nombre de la categoria
        """
        data = self.get_queryset()
        data = self.get_serializer(data, many=True)
        return Response(data.data)

    
    

class IndicatorViewSet(viewsets.ModelViewSet):
    serializer_class = IndicatorSerializer
    queryset = IndicatorSerializer.Meta.model.objects.filter(state=True)

    