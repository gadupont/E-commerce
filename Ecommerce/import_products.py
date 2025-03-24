import json
from shop.models import Product


with open('./../products.json') as f:
    products_data = json.load(f)


for product_data in products_data:
    Product.objects.create(
        id=product_data['id'],
        name=product_data['name'],
        price=product_data['price'],
        description=product_data['description'],
        category=product_data['category']
    )
