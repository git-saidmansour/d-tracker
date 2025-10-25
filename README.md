# 💰 D-Tracker - Suivi des Dépenses

Une application web moderne pour le suivi et l'analyse de vos dépenses personnelles, développée avec Streamlit.

## 🚀 Fonctionnalités

### 📊 Tableau de Bord
- Vue d'ensemble avec métriques clés
- Filtres temporels (jour, semaine, mois, année, personnalisé)
- Graphiques interactifs par catégorie et période
- Statistiques en temps réel

### ➕ Gestion des Dépenses
- Enregistrement simple et rapide
- Catégorisation automatique (8 catégories prédéfinies)
- Interface intuitive avec formulaire optimisé

### 📈 Analyses Avancées
- Graphiques par catégorie (camembert, barres)
- Évolution temporelle (jour, semaine, mois)
- Tableaux détaillés avec export CSV
- Filtres personnalisables

### 📋 Historique Complet
- Consultation de toutes les transactions
- Filtres par date et catégorie
- Export des données en CSV
- Recherche et tri avancés

## 🛠️ Installation

1. **Cloner le projet**
```bash
git clone <votre-repo>
cd d-tracker
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Lancer l'application**
```bash
streamlit run app.py
```

## 📱 Utilisation

1. **Première utilisation** : L'application crée automatiquement la base de données SQLite
2. **Ajouter une dépense** : Utilisez l'onglet "Nouvelle Dépense"
3. **Consulter les analyses** : Naviguez dans les différents onglets
4. **Exporter vos données** : Utilisez la fonction d'export CSV

## 🗂️ Structure du Projet

```
d-tracker/
├── app.py              # Application Streamlit principale
├── database.py         # Gestion de la base de données SQLite
├── requirements.txt    # Dépendances Python
├── expenses.db         # Base de données SQLite (créée automatiquement)
└── README.md          # Documentation
```

## 🎨 Catégories Prédéfinies

- 🍽️ **Alimentation** - Restaurants, courses, snacks
- 🚗 **Transport** - Essence, transports en commun, taxi
- 🏠 **Logement** - Loyer, charges, réparations
- 🏥 **Santé** - Médecin, pharmacie, mutuelle
- 🎮 **Loisirs** - Cinéma, sport, sorties
- 🛍️ **Shopping** - Vêtements, électronique, divers
- 📚 **Éducation** - Livres, formations, cours
- 📦 **Autres** - Dépenses diverses

## 🔧 Personnalisation

### Ajouter une nouvelle catégorie
Modifiez le fichier `database.py` dans la section `default_categories`.

### Modifier l'interface
Éditez le fichier `app.py` pour personnaliser les couleurs, textes et layout.

## 📊 Base de Données

L'application utilise SQLite avec deux tables principales :
- `categories` : Stockage des catégories de dépenses
- `expenses` : Enregistrement des transactions

## 🚀 Déploiement

Pour déployer sur Streamlit Cloud :
1. Poussez votre code sur GitHub
2. Connectez-vous à [share.streamlit.io](https://share.streamlit.io)
3. Sélectionnez votre repository
4. L'application sera déployée automatiquement

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer de nouvelles fonctionnalités
- Améliorer la documentation
- Optimiser le code

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

---

Développé par Saîd & Maqs
