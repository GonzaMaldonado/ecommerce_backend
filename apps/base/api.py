from rest_framework import generics

class GeneralListAPIView(generics.ListAPIView):
    serializer_class = None

    def get_queryset(self):
        #Estoy obteniendo el serializador y este tiene una clase Meta el cual tiene mi modelo - gral_seria.py
        model = self.get_serializer().Meta.model
        # Y asi obtengo todos los modelos que hereden de esta clase y los filtro por su estado
        return model.objects.filter(state=True)