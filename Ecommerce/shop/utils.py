import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
from django.apps import apps

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

    return matrix, product_ids, pid_to_idx

def build_svd_matrix(matrix, n_components=50):
    """
    Applique SVD pour réduire la dimension de la matrice produit-commande.
    """
    svd = TruncatedSVD(n_components=n_components)
    matrix_svd = svd.fit_transform(matrix)  # Réduit la matrice
    return matrix_svd

def build_similarity_matrix(matrix_svd=None, matrix=None):
    """
    Calcule la matrice de similarité.
    Si matrix_svd est passé, utilise la matrice réduite par SVD,
    sinon calcule la similarité en utilisant la matrice complète.
    """
    if matrix_svd is not None:
        return cosine_similarity(matrix_svd)  # Similarité cosinus sur la matrice SVD
    elif matrix is not None:
        return cosine_similarity(matrix)  # Similarité cosinus sur la matrice brute
    return None

def get_similarity_data(use_svd=True):
    """
    Récupère la matrice de similarité en fonction du paramètre `use_svd`.
    Si `use_svd` est True, utilise SVD pour réduire la dimension.
    Si False, utilise la matrice brute pour calculer la similarité.
    """
    matrix, product_ids, pid_to_idx = build_collaborative_matrix()

    if use_svd:
        matrix_svd = build_svd_matrix(matrix)
        similarity_matrix = build_similarity_matrix(matrix_svd=matrix_svd)
    else:
        similarity_matrix = build_similarity_matrix(matrix=matrix)

    return similarity_matrix, product_ids, pid_to_idx

def recommander_produits(panier, top_n=4, use_svd=True):
    """
    Recommande des produits similaires en utilisant la similarité cosinus.
    panier : liste d'entiers (IDs des produits)
    top_n : nombre de recommandations à retourner
    use_svd : True pour utiliser la réduction SVD, False pour ne pas l'utiliser
    Retourne : liste d'IDs de produits recommandés
    """
    similarity_matrix, product_ids, pid_to_idx = get_similarity_data(use_svd)

    if not panier:
        return []

    scores = np.zeros(len(product_ids))
    for pid in panier:
        if pid in pid_to_idx:
            scores += similarity_matrix[pid_to_idx[pid]]

    sorted_indices = np.argsort(scores)[::-1]
    
    recommendations = [
        product_ids[i] for i in sorted_indices 
        if product_ids[i] not in panier
    ][:top_n]

    return recommendations
