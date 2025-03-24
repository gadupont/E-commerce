import json
from shop.models import Order, Product, OrderProduct


with open('./../orders.json') as f:
    orders_data = json.load(f)

# Insère chaque commande dans la base de données
for order_data in orders_data:
    order = Order(email=f"client{order_data['client_id']}@example.com")  # Générer un email basé sur l'ID client
    order.save()

    # Associe les produits et quantités à chaque commande
    for product_data in order_data['products']:
        product = Product.objects.get(id=product_data['product_id'])
        quantity = product_data['quantity']
        OrderProduct.objects.create(order=order, product=product, quantity=quantity)

print("Commandes insérées avec succès !")
