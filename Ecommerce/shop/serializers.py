from rest_framework import serializers
from .models import Product, Order, OrderProduct

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductOrderSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), 
        source='product'  # Map to the 'product' ForeignKey in OrderProduct
    )
    quantity = serializers.IntegerField()

    class Meta:
        model = OrderProduct
        fields = ['product_id', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    products = ProductOrderSerializer(
        many=True, 
        source='orderproduct_set'  # Use the reverse relation to OrderProduct
    )

    class Meta:
        model = Order
        fields = ['email', 'products']

    def create(self, validated_data):
        products_data = validated_data.pop('orderproduct_set')  # Extract products data
        order = Order.objects.create(email=validated_data['email'])  # Create the order

        # Create OrderProduct entries for each product
        for product_data in products_data:
            product = product_data['product']  # Product instance from PrimaryKeyRelatedField
            quantity = product_data['quantity']
            OrderProduct.objects.create(order=order, product=product, quantity=quantity)

        return order
    


class RecommendationSerializer(serializers.Serializer):
    panier = serializers.ListField(child=serializers.IntegerField())


class ProductWithQuantitySerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    product_id = serializers.IntegerField(source='product.id')
    quantity = serializers.IntegerField()

    class Meta:
        model = OrderProduct
        fields = ['product_id', 'product_name', 'quantity']
