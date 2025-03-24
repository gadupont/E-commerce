from django.shortcuts import render

# Create your views here.


from rest_framework import generics , status 
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product , Order , OrderProduct
from .serializers import ProductSerializer, OrderSerializer, RecommendationSerializer
from .utils import recommander_produits


# Vue pour lister tous les produits
class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()  # Liste tous les produits
    serializer_class = ProductSerializer  # Utilise le serializer ProductSerializer




class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        # Crée la commande avec le serializer
        order = serializer.save()

        # Les produits ont déjà été ajoutés via le serializer, donc pas besoin de les ajouter à la main ici
        return order
    




class ProductRecommendationView(APIView):
    def post(self, request):
        
        panier = request.data.get('panier')
        
        
        # Récupérer les recommandations en fonction du panier
        recommended_products_ids = recommander_produits(panier)

        recommended_products = Product.objects.filter(id__in=recommended_products_ids)
        
        # Préparer les données à renvoyer
        recommended_product_names = [product.name for product in recommended_products]
        
        return Response({"recommended_products": recommended_product_names}, status=status.HTTP_200_OK)