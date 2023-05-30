from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializer import UserSerializer, UserUpdateSerializer, PasswordSerializer, UserListSerializer

class UserViewSet(viewsets.GenericViewSet):
    serializer_class = UserSerializer
    list_serializer_class = UserListSerializer

    def get_object(self, pk):
        return get_object_or_404(self.serializer_class.Meta.model, pk=pk)


    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.serializer_class().Meta.model.objects\
                            .filter(is_active=True).values('id', 'name', 'username', 'email')
        return self.queryset
    
    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        user = self.get_object(pk)
        password_serializer = PasswordSerializer(data=request.data)
        if password_serializer.is_valid():
            user.set_password(password_serializer.validated_data['password'])
            user.save()
            return Response({'message': 'Contraseña actualizada correctamente'})
        return Response({'message': 'Hay errores en la información enviada',
                         'error': password_serializer.errors},
                         status=status.HTTP_400_BAD_REQUEST)
        

    def list(self, request):
        users = self.get_queryset()
        users_serializer = self.list_serializer_class(users, many=True)
        return Response(users_serializer.data)
    
    
    def create(self, request):
        user_serializer = self.serializer_class(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({'message': 'Usuario creado correctamente', 'user': user_serializer.data}, 
                            status=status.HTTP_201_CREATED)
        return Response({'message': 'Existen errores en el registro', 'error': user_serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)
    

    def retrieve(self, request,*args,**kwargs):
            user = self.get_object(kwargs['pk'])
            if user:
                user_serializer = self.serializer_class(user)
                return Response(user_serializer.data)
            return Response({'error': 'Usuario no encontrado'},status=status.HTTP_404_NOT_FOUND)
      
    
    def update(self, request, pk=None):
        user = self.get_object(pk)
        user_serializer = UserUpdateSerializer(user, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({'message': 'usuario actualizado correctamente','user': user_serializer.data})
        return Response({'message': 'Hubo errores en la actualización', 'error': user_serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)
    

    def destroy(self, request, pk=None):
        user = self.serializer_class.Meta.model.objects.filter(id=pk).update(is_active=False)
        if user == 1:
            return Response({'message': 'Usario eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        

