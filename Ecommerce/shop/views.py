from django.shortcuts import render
from rest_framework import generics , status 
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product , Order , OrderProduct
from .serializers import ProductSerializer, OrderSerializer, RecommendationSerializer , ProductWithQuantitySerializer
from .utils import recommander_produits


class ProductListView(generics.ListCreateAPIView):
    """
    Cette vue permet de lister tous les produits ou d'en créer un nouveau.
    Utilise le sérialiseur ProductSerializer pour gérer les données des produits.
    """
    queryset = Product.objects.all()  # Liste tous les produits
    serializer_class = ProductSerializer  # Utilise le serializer ProductSerializer




class OrderCreateView(generics.CreateAPIView):
    """
    Cette vue permet de créer une nouvelle commande.
    Utilise le sérialiseur OrderSerializer pour gérer la création de la commande.
    Les produits associés sont automatiquement ajoutés via le serializer.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        """
        Crée la commande avec le serializer.
        Les produits ont déjà été ajoutés via le serializer, donc pas besoin de les ajouter ici.
        """
        order = serializer.save()
        return order
    




class ProductRecommendationView(APIView):
    """
    Cette vue permet de recommander des produits basés sur un panier donné.
    Utilise la fonction recommander_produits pour obtenir les produits recommandés.
    """
    def post(self, request):
        
        panier = request.data.get('panier')
        
        
        # Récupérer les recommandations en fonction du panier
        recommended_products_ids = recommander_produits(panier)


        recommended_products = Product.objects.filter(id__in=recommended_products_ids)
        
        # Préparer les données à renvoyer
        recommended_product_names = [product.name for product in recommended_products]
        
        return Response({"recommended_products": recommended_product_names}, status=status.HTTP_200_OK)
    



class OrderProductsView(APIView):
    """
    Récupère les produits associés à une commande donnée, avec leur quantité.
    """
    def get(self, request, order_id):
        try:
            # Récupérer la commande en question
            order = Order.objects.get(id=order_id)

            # Récupérer les produits associés à la commande
            order_products = order.orderproduct_set.all()
            
            # Sérialiser les produits associés à la commande avec leur quantité
            serializer = ProductWithQuantitySerializer(order_products, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)