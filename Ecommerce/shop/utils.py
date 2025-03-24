import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from django.apps import apps
from collections import defaultdict

def build_collaborative_matrix():
    
    OrderProduct = apps.get_model('shop', 'OrderProduct')
    Product = apps.get_model('shop', 'Product')

    # Récupérer tous les produits et commandes
    all_products = Product.objects.all()
    all_orders = OrderProduct.objects.values('order_id').distinct()

    product_ids = [p.id for p in all_products]
    order_ids = [o['order_id'] for o in all_orders]

    # Dictionnaire pour mapper les IDs aux indices
    pid_to_idx = {pid: i for i, pid in enumerate(product_ids)}
    oid_to_idx = {oid: i for i, oid in enumerate(order_ids)}

    # Construire la matrice produit-commande
    matrix = np.zeros((len(product_ids), len(order_ids)))
    for op in OrderProduct.objects.select_related('product', 'order'):
        pid = op.product.id
        oid = op.order.id
        matrix[pid_to_idx[pid]][oid_to_idx[oid]] = op.quantity

    # Calculer la matrice de similarité cosinus
    similarity_matrix = cosine_similarity(matrix)

    return similarity_matrix, product_ids, pid_to_idx

# Cache global (à améliorer avec un vrai cache comme Redis si besoin)
_similarity_data = None

def get_similarity_data():
    global _similarity_data
    if _similarity_data is None:
        _similarity_data = build_collaborative_matrix()
    return _similarity_data

def recommander_produits(panier, top_n=3):
    """
    Recommande des produits similaires à ceux dans le panier.
    panier : liste d'entiers (IDs des produits)
    Retourne : liste d'IDs de produits recommandés
    """
    # Récupérer la matrice de similarité et les mappings
    similarity_matrix, product_ids, pid_to_idx = get_similarity_data()

    # Si le panier est vide, retourner une liste vide ou des produits populaires
    if not panier:
        return []

    # Calculer un score pour chaque produit basé sur les similarités
    scores = np.zeros(len(product_ids))
    for pid in panier:
        if pid in pid_to_idx:
            scores += similarity_matrix[pid_to_idx[pid]]

    # Trier les produits par score décroissant
    sorted_indices = np.argsort(scores)[::-1]
    
    # Exclure les produits déjà dans le panier et limiter à top_n
    recommendations = [
        product_ids[i] for i in sorted_indices 
        if product_ids[i] not in panier
    ][:top_n]

    return recommendations

