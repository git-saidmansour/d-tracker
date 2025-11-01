#!/usr/bin/env python3
"""
Script pour ajouter des données d'exemple au D-Tracker
Génère des dépenses réalistes sur les deux dernières années
"""

import sqlite3
import random
from datetime import datetime, timedelta
from database import ExpenseDatabase

def add_sample_data():
    """Ajoute des données d'exemple réalistes"""
    
    # Initialiser la base de données
    db = ExpenseDatabase()
    
    # Récupérer les catégories
    categories = db.get_categories()
    category_dict = {cat[1]: cat[0] for cat in categories}
    
    # Descriptions réalistes par catégorie
    descriptions = {
        'Alimentation': [
            'Déjeuner au restaurant', 'Courses Carrefour', 'Petit-déjeuner café', 
            'Dîner avec amis', 'Commande Uber Eats', 'Sandwich midi',
            'Courses bio', 'Restaurant italien', 'Fast-food', 'Épicerie'
        ],
        'Nourriture': [
            'Déjeuner au restaurant', 'Courses Carrefour', 'Petit-déjeuner café', 
            'Dîner avec amis', 'Commande Uber Eats', 'Sandwich midi',
            'Courses bio', 'Restaurant italien', 'Fast-food', 'Épicerie'
        ],
        'Transport': [
            'Essence station', 'Ticket métro', 'Parking centre-ville', 
            'Taxi aéroport', 'Abonnement transport', 'Réparation voiture',
            'Vignette autoroute', 'Bus urbain', 'Vélo partagé', 'Covoiturage'
        ],
        'Logement': [
            'Loyer mensuel', 'Charges copropriété', 'Électricité', 
            'Internet/Box', 'Assurance habitation', 'Réparation robinet',
            'Nettoyage vitres', 'Décoration salon', 'Plomberie', 'Éclairage'
        ],
        'Santé': [
            'Consultation médecin', 'Pharmacie', 'Dentiste', 
            'Mutuelle santé', 'Optique lunettes', 'Kinésithérapeute',
            'Médicaments', 'Analyses médicales', 'Podologue', 'Psychologue'
        ],
        'Loisirs': [
            'Cinéma', 'Abonnement Netflix', 'Livre librairie', 
            'Concert', 'Musée', 'Sport salle', 'Jeu vidéo', 
            'Théâtre', 'Piscine', 'Bowling'
        ],
        'Shopping': [
            'Vêtements Zara', 'Chaussures', 'Électronique', 
            'Cosmétiques', 'Bricolage', 'Jouets enfants', 
            'Accessoires', 'Parfum', 'Montre', 'Sac à main'
        ],
        'Éducation': [
            'Livre technique', 'Formation en ligne', 'Cours particuliers', 
            'Matériel scolaire', 'Conférence', 'Abonnement revue',
            'Stage professionnel', 'Certification', 'Manuel université', 'Kit électronique'
        ],
        'Autres': [
            'Cadeau anniversaire', 'Réparation électroménager', 
            'Dons association', 'Frais bancaires', 'Timbres',
            'Coiffeur', 'Nettoyage voiture', 'Pet-sitting', 
            'Déménagement', 'Divers'
        ]
    }
    
    # Générer des dépenses sur les deux dernières années (730 jours)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)
    
    print("🔄 Génération des données d'exemple sur 2 ans...")
    
    expenses_added = 0
    total_days = 730
    
    # Pour chaque jour sur 2 ans
    for day in range(total_days + 1):  # +1 pour inclure aujourd'hui
        current_date = start_date + timedelta(days=day)
        date_str = current_date.strftime("%Y-%m-%d")
        
        # Nombre de dépenses par jour (0-4, plus probable d'avoir 1-2)
        # Réduire légèrement la probabilité d'avoir des dépenses pour certaines dates
        num_expenses = random.choices([0, 1, 2, 3, 4], weights=[15, 35, 30, 15, 5])[0]
        
        for _ in range(num_expenses):
            # Sélectionner une catégorie aléatoire
            category_name = random.choice(list(category_dict.keys()))
            category_id = category_dict[category_name]
            
            # Montant réaliste selon la catégorie
            if category_name in ['Alimentation', 'Nourriture']:
                amount = round(random.uniform(5, 50), 2)
            elif category_name == 'Transport':
                amount = round(random.uniform(10, 80), 2)
            elif category_name == 'Logement':
                amount = round(random.uniform(20, 200), 2)
            elif category_name == 'Santé':
                amount = round(random.uniform(15, 120), 2)
            elif category_name == 'Loisirs':
                amount = round(random.uniform(8, 60), 2)
            elif category_name == 'Shopping':
                amount = round(random.uniform(15, 150), 2)
            elif category_name == 'Éducation':
                amount = round(random.uniform(10, 80), 2)
            else:  # Autres
                amount = round(random.uniform(5, 100), 2)
            
            # Description aléatoire (avec fallback pour les catégories non définies)
            if category_name in descriptions:
                description = random.choice(descriptions[category_name])
            else:
                # Fallback pour les catégories non définies
                description = f"Dépense {category_name.lower()}"
            
            # Ajouter la dépense
            try:
                db.add_expense(amount, description, category_id, date_str)
                expenses_added += 1
            except Exception as e:
                print(f"❌ Erreur lors de l'ajout de la dépense : {e}")
    
    print(f"✅ {expenses_added} dépenses d'exemple ajoutées avec succès sur 2 ans !")
    
    # Afficher quelques statistiques
    print("\n📊 Statistiques générées :")
    
    # Total général
    total = db.get_total_expenses()
    print(f"💰 Total des dépenses : {total:.2f} €")
    
    # Dépenses d'aujourd'hui
    today = datetime.now().strftime("%Y-%m-%d")
    today_total = db.get_total_expenses(today, today)
    print(f"📅 Dépenses d'aujourd'hui : {today_total:.2f} €")
    
    # Nombre de transactions
    all_expenses = db.get_expenses()
    print(f"📝 Nombre total de transactions : {len(all_expenses)}")
    
    # Top 3 catégories
    category_stats = db.get_stats_by_category()
    if len(category_stats) > 0:
        print(f"\n🏆 Top 3 catégories :")
        for i, (_, row) in enumerate(category_stats.head(3).iterrows()):
            print(f"  {i+1}. {row['category']} : {row['total']:.2f} €")

if __name__ == "__main__":
    add_sample_data()

