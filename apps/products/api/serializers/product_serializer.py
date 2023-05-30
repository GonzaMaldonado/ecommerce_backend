from rest_framework import serializers
from apps.products.models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        exclude = ('state', 'created', 'updated', 'deleted')


    def create(self, validated_data):
        if validated_data['image'] == None:
            validated_data['image'] = ''
        return Product.objects.create(**validated_data)
    

#Con este validate estoy forzando el campo measure_unit, pq en mi modelo puse que podia ser un campo null
    def validate_measure_unit(self, value):
        if value == '' or value == None:
            raise serializers.ValidationError({'error': 'Debe ingresar una unidad de medida'})
        return value
    
    def validate_category_product(self, value):
        if value == '' or value == None:
            raise serializers.ValidationError({'error': 'Debe ingresar una categoría al producto'})
        return value
    
    def validate(self, value):
        if 'measure_unit' not in value.keys():
            raise serializers.ValidationError({'measure_unit': 'Debe ingresar una unidad de medida'})
        
        if 'category_product' not in value.keys():
            raise serializers.ValidationError({'category_product': 'Debe ingresar una categoria al producto'})
        return value


    #Utilizo este metodo para que en lugar de mostrarme las Nros de las llaves foraneas de los dos 
    #últimos campos, en su lugar, me muestre su descipcion
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.name,
            'description': instance.description,
            'image': instance.image.url if instance.image != '' else '',
            'measure_unit': instance.measure_unit.description if instance.measure_unit is not None else '',
            'category_product': instance.category_product.description if instance.category_product is not None else ''
        }
