# D-Tracker - Suivi des Dépenses

Une application web moderne pour le suivi et l'analyse de vos dépenses personnelles, développée avec Streamlit.

## Fonctionnalités

### Tableau de Bord
- Vue d'ensemble avec métriques clés
- Filtres temporels (jour, semaine, mois, année, tout)
- Graphiques interactifs par catégorie et période
- Statistiques en temps réel avec comparaisons

### Gestion des Dépenses
- Enregistrement simple et rapide
- Catégorisation automatique (8 catégories prédéfinies)
- Interface intuitive avec formulaire optimisé

### Analyses Avancées
- Graphiques par catégorie (camembert, barres)
- Évolution temporelle en courbes par catégorie
- Sélection de période et catégories personnalisables
- Tableaux détaillés avec export CSV

### Historique Complet
- Consultation de toutes les transactions
- Filtres par date et catégorie
- Export des données en CSV
- Recherche et tri avancés

### Gestion des Catégories
- Création de nouvelles catégories
- Modification des catégories existantes
- Suppression de catégories (avec vérification des dépendances)

## Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner le projet**
```bash
git clone https://github.com/git-saidmansour/d-tracker.git
cd d-tracker
```

2. **Créer un environnement virtuel (recommandé)**
```bash
python -m venv venv
source venv/bin/activate  # Sur Linux/Mac
# ou
venv\Scripts\activate  # Sur Windows
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Remplir la base de données avec des données d'exemple (optionnel)**
```bash
python add_sample_data.py
```

Ce script génère des dépenses réalistes sur les 30 derniers jours pour vous permettre de tester toutes les fonctionnalités de l'application immédiatement. La base de données sera créée automatiquement lors du premier lancement ou lors de l'exécution de ce script.

5. **Lancer l'application**
```bash
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse `http://localhost:8501`

## Utilisation

### Première utilisation

1. L'application crée automatiquement la base de données SQLite `expenses.db` lors du premier lancement
2. Si vous souhaitez commencer avec des données d'exemple, exécutez `python add_sample_data.py` avant de lancer l'application
3. Les catégories par défaut sont automatiquement créées lors de l'initialisation

### Navigation dans l'application

- **Accueil** : Page de bienvenue
- **Dashboard** : Tableau de bord principal avec vue d'ensemble et graphiques
- **Nouvelle Dépense** : Formulaire pour enregistrer une nouvelle dépense
- **Analyses** : Analyses détaillées avec graphiques interactifs
- **Historique** : Liste complète de toutes les transactions
- **Catégories** : Gestion des catégories de dépenses

### Enregistrer une dépense

1. Allez dans l'onglet "Nouvelle Dépense"
2. Remplissez le formulaire :
   - Montant (en euros)
   - Date (par défaut aujourd'hui)
   - Catégorie (sélection parmi les catégories disponibles)
   - Description (optionnelle)
3. Cliquez sur "Enregistrer la Dépense"

## Structure du Projet

```
d-tracker/
├── app.py                      # Application Streamlit principale (page d'accueil)
├── database.py                 # Gestion de la base de données SQLite
├── add_sample_data.py          # Script pour générer des données d'exemple
├── requirements.txt            # Dépendances Python
├── expenses.db                 # Base de données SQLite (créée automatiquement)
├── .streamlit/
│   └── config.toml             # Configuration Streamlit (thème par défaut)
├── pages/
│   ├── dashboard.py            # Page du tableau de bord
│   ├── nouvelle_dépense.py     # Page d'ajout de dépense
│   ├── analyses.py             # Page d'analyses détaillées
│   ├── history.py              # Page d'historique des transactions
│   └── categories.py           # Page de gestion des catégories
├── components/
│   ├── charts.py               # Composants de graphiques
│   └── metrics.py              # Composants de métriques
├── config/
│   └── settings.py             # Configuration de l'application
└── utils/
    ├── date_utils.py           # Utilitaires de manipulation de dates
    └── formatters.py           # Utilitaires de formatage
```

## Catégories Prédéfinies

L'application inclut 8 catégories par défaut :

- **Alimentation** - Restaurants, courses, snacks
- **Transport** - Essence, transports en commun, taxi
- **Logement** - Loyer, charges, réparations
- **Santé** - Médecin, pharmacie, mutuelle
- **Loisirs** - Cinéma, sport, sorties
- **Shopping** - Vêtements, électronique, divers
- **Éducation** - Livres, formations, cours
- **Autres** - Dépenses diverses

Vous pouvez créer, modifier et supprimer des catégories depuis l'interface de l'application.

## Base de Données

L'application utilise SQLite avec deux tables principales :

- `categories` : Stockage des catégories de dépenses (id, name, color)
- `expenses` : Enregistrement des transactions (id, amount, description, category_id, date)

La base de données est créée automatiquement lors du premier lancement de l'application. Le fichier `expenses.db` est stocké localement dans le répertoire du projet.

## Script de données d'exemple

Le fichier `add_sample_data.py` permet de remplir la base de données avec des dépenses d'exemple réalistes sur les 30 derniers jours. Ce script est utile pour :

- Tester toutes les fonctionnalités de l'application
- Visualiser les graphiques avec des données variées
- Comprendre le fonctionnement de l'application sans avoir à saisir manuellement de nombreuses dépenses

Pour utiliser ce script :
```bash
python add_sample_data.py
```

Le script affichera le nombre de dépenses générées et quelques statistiques.

## Déploiement

### Streamlit Cloud

Pour déployer sur Streamlit Cloud :

1. Poussez votre code sur GitHub
2. Connectez-vous à [share.streamlit.io](https://share.streamlit.io)
3. Sélectionnez votre repository
4. Configurez le fichier principal comme `app.py`
5. L'application sera déployée automatiquement

### Local

L'application peut également être exécutée localement avec la commande :
```bash
streamlit run app.py
```

## Configuration

### Thème

Le thème par défaut est défini dans `.streamlit/config.toml`. Vous pouvez modifier le thème (light/dark/system) directement depuis l'interface Streamlit ou en modifiant le fichier de configuration.

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

- Signaler des bugs
- Proposer de nouvelles fonctionnalités
- Améliorer la documentation
- Optimiser le code

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

---

Développé par Saîd Mansour et Max Guiriec.
