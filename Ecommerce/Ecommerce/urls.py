"""
URL configuration for Ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from shop import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', views.ProductListView.as_view(), name='product-list'),  # Liste des produits
    path('orders/', views.OrderCreateView.as_view(), name='order-create'),  # Création d'une commande
    path('recommendations/', views.ProductRecommendationView.as_view(), name='product-recommendations'),
    path('orders/<int:order_id>/products/', views.OrderProductsView.as_view(), name='order-products'),
]
