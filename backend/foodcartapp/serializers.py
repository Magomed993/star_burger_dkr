from rest_framework.serializers import ModelSerializer
from foodcartapp.models import Product, Order, OrderElement


class OrderElementSerializer(ModelSerializer):
    class Meta:
        model = OrderElement
        fields = ['product', 'quantity']


class OrderSerializer(ModelSerializer):
    products = OrderElementSerializer(many=True, allow_empty=False, write_only=True)
    class Meta:
        model = Order
        fields = ['id', 'address', 'firstname', 'lastname', 'phonenumber', 'products']

    def create(self, validated_data):
        products_serializer = validated_data['products']

        for item in products_serializer:
            product = Product.objects.filter(name=item.get('product')).first()
            order, created = Order.objects.get_or_create(
                address=validated_data['address'],
                firstname=validated_data['firstname'],
                lastname=validated_data['lastname'],
                phonenumber=validated_data['phonenumber']
            )
            order_element, el_created = OrderElement.objects.get_or_create(
                order=order,
                product=product,
                defaults={
                    'quantity': item['quantity'],
                    'price': product.price * item['quantity']
                }
            )
        return order
