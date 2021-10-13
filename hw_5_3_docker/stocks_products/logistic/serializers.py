from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from logistic.models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    # настройте сериализатор для позиции продукта на складе
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    def validate_positions(self, value):
        if not value:
            raise ValidationError('пустой список продуктов')
        return value

    def create(self, validated_data):
        positions = validated_data.pop('positions')

        stock = super().create(validated_data)

        for item in positions:
            StockProduct.objects.create(stock=stock, **item)

        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')

        stock = super().update(instance, validated_data)

        for item in positions:
            StockProduct.objects.update_or_create(stock=instance, product=item["product"], defaults={**item})

        return stock
