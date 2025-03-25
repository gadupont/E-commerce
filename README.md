# E-commerce Product Recommendation System

Ce projet implémente un système de recommandations de produits pour un e-commerce en utilisant une techniques de filtrage collaboratif avec réduction de dimensionnalité (SVD) et similarité cosinus.

## Prérequis

- Python 3.x
- Django

## Installation

### 1. Cloner le repository

Clonez ce repository :


git clone https://github.com/gadupont/E-commerce.git


### 2. Créer et activer un environnement virtuel

python -m venv venv

source venv/bin/activate  # Sur Windows, utilisez `venv\Scripts\activate`


### 3. Installer les dépendances

pip install -r requirements.txt



### 4. Lancer le serveur Django

cd .\Ecommerce\

python manage.py runserver

Le serveur sera accessible à l'adresse suivante : http://localhost:8000


### 5. Utilisation de l'API


L'API permet de :

Récupérer les produits d'une commande : Vous pouvez tester l'API pour récupérer la liste des produits associés à une commande en particulier avec 
curl -X GET http://localhost:8000/orders/order_ID/products/       avec order_ID étant le numéro de la commande


Créer une commande : Vous pouvez envoyer une requête POST pour créer une commande avec des produits associés avec le format suivant 
curl -X POST http://localhost:8000/orders/ -H "Content-Type: application/json" -d "{\"email\":\"test@example.com\",\"products\":[{\"product_id\":1,\"quantity\":2},{\"product_id\":2,\"quantity\":1}]}"


Obtenir des recommandations de produits : En envoyant un panier d'articles, l'API retourne une liste de produits recommandés basés sur la similarité des produits.

example : curl -X POST "http://localhost:8000/recommendations/" -H "Content-Type: application/json" -d "{\"panier\": [1, 2, 3]}"



## Améliorations possibles

### Utilisation de modèles de Machine Learning

Le système de recommandation actuel repose sur une approche de filtrage collaboratif basée sur la similarité cosinus. Toutefois, si le nombre de commande est plus important il serait intéressant de passer à un modèle de machine learning.

Cependant, étant donné que la quantité actuelle de commandes est insuffisante pour entraîner de manière efficace un tel modèle, cette approche n'a pas encore été implémentée. Cela pourrait être un axe d'amélioration pour le futur une fois que suffisamment de données seront disponibles.

### système de notation

Intégrer d'un système de notation pour les produits, afin de personnaliser encore plus les recommandations.

 
