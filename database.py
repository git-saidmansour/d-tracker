import sqlite3
import pandas as pd
from datetime import datetime
import os

class ExpenseDatabase:
    def __init__(self, db_path="expenses.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialise la base de données avec les tables nécessaires"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Table des catégories
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                color TEXT DEFAULT '#1f77b4'
            )
        ''')
        
        # Table des dépenses
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                description TEXT,
                category_id INTEGER,
                date TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories (id)
            )
        ''')
        
        # Insérer les catégories par défaut
        default_categories = [
            ('Alimentation', '#ff7f0e'),
            ('Transport', '#2ca02c'),
            ('Logement', '#d62728'),
            ('Santé', '#9467bd'),
            ('Loisirs', '#8c564b'),
            ('Shopping', '#e377c2'),
            ('Éducation', '#7f7f7f'),
            ('Autres', '#bcbd22')
        ]
        
        for name, color in default_categories:
            cursor.execute('''
                INSERT OR IGNORE INTO categories (name, color) VALUES (?, ?)
            ''', (name, color))
        
        conn.commit()
        conn.close()
    
    def add_expense(self, amount, description, category_id, date):
        """Ajoute une nouvelle dépense"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO expenses (amount, description, category_id, date)
            VALUES (?, ?, ?, ?)
        ''', (amount, description, category_id, date))
        
        conn.commit()
        conn.close()
        return cursor.lastrowid
    
    def get_expenses(self, start_date=None, end_date=None, category_name=None):
        """Récupère les dépenses avec filtres optionnels"""
        conn = sqlite3.connect(self.db_path)
        
        query = '''
            SELECT e.id, e.amount, e.description, e.date, c.name as category, c.color
            FROM expenses e
            LEFT JOIN categories c ON e.category_id = c.id
        '''
        
        params = []
        conditions = []
        
        if start_date:
            conditions.append('e.date >= ?')
            params.append(start_date)
        if end_date:
            conditions.append('e.date <= ?')
            params.append(end_date)
        if category_name:
            conditions.append('c.name = ?')
            params.append(category_name)
        
        if conditions:
            query += ' WHERE ' + ' AND '.join(conditions)
        
        query += ' ORDER BY e.date DESC'
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df
    
    def get_categories(self):
        """Récupère toutes les catégories"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, name, color FROM categories ORDER BY name')
        categories = cursor.fetchall()
        conn.close()
        return categories
    
    def get_stats_by_period(self, period='month'):
        """Récupère les statistiques par période"""
        conn = sqlite3.connect(self.db_path)
        
        if period == 'day':
            query = '''
                SELECT date, SUM(amount) as total
                FROM expenses
                GROUP BY date
                ORDER BY date DESC
            '''
        elif period == 'week':
            query = '''
                SELECT strftime('%Y-%W', date) as week, SUM(amount) as total
                FROM expenses
                GROUP BY strftime('%Y-%W', date)
                ORDER BY week DESC
            '''
        elif period == 'month':
            query = '''
                SELECT strftime('%Y-%m', date) as month, SUM(amount) as total
                FROM expenses
                GROUP BY strftime('%Y-%m', date)
                ORDER BY month DESC
            '''
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    
    def get_stats_by_category(self, start_date=None, end_date=None):
        """Récupère les statistiques par catégorie"""
        conn = sqlite3.connect(self.db_path)
        
        query = '''
            SELECT c.name as category, c.color, SUM(e.amount) as total, COUNT(e.id) as count
            FROM expenses e
            LEFT JOIN categories c ON e.category_id = c.id
        '''
        
        params = []
        if start_date or end_date:
            query += ' WHERE'
            conditions = []
            if start_date:
                conditions.append('e.date >= ?')
                params.append(start_date)
            if end_date:
                conditions.append('e.date <= ?')
                params.append(end_date)
            query += ' ' + ' AND '.join(conditions)
        
        query += '''
            GROUP BY c.id, c.name, c.color
            ORDER BY total DESC
        '''
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df
    
    def get_total_expenses(self, start_date=None, end_date=None):
        """Calcule le total des dépenses"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = 'SELECT SUM(amount) FROM expenses'
        params = []
        
        if start_date or end_date:
            query += ' WHERE'
            conditions = []
            if start_date:
                conditions.append('date >= ?')
                params.append(start_date)
            if end_date:
                conditions.append('date <= ?')
                params.append(end_date)
            query += ' ' + ' AND '.join(conditions)
        
        cursor.execute(query, params)
        total = cursor.fetchone()[0] or 0
        conn.close()
        return total
    
    def add_category(self, name, color):
        """Ajoute une nouvelle catégorie"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO categories (name, color)
            VALUES (?, ?)
        ''', (name, color))
        
        conn.commit()
        conn.close()
        return cursor.lastrowid
    
    def update_category(self, category_id, name, color):
        """Met à jour une catégorie"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE categories 
            SET name = ?, color = ?
            WHERE id = ?
        ''', (name, color, category_id))
        
        conn.commit()
        conn.close()
    
    def delete_category(self, category_id):
        """Supprime une catégorie"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Vérifier s'il y a des dépenses associées
        cursor.execute('SELECT COUNT(*) FROM expenses WHERE category_id = ?', (category_id,))
        count = cursor.fetchone()[0]
        
        if count > 0:
            conn.close()
            return False, f"Il y a {count} dépense(s) associée(s) à cette catégorie. Impossible de la supprimer."
        
        cursor.execute('DELETE FROM categories WHERE id = ?', (category_id,))
        conn.commit()
        conn.close()
        return True, "Catégorie supprimée avec succès"
    
    def get_category_by_id(self, category_id):
        """Récupère une catégorie par son ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, name, color FROM categories WHERE id = ?', (category_id,))
        category = cursor.fetchone()
        conn.close()
        return category
    
    def get_daily_expenses(self, start_date, end_date):
        """Récupère les dépenses quotidiennes pour une période donnée"""
        conn = sqlite3.connect(self.db_path)
        
        query = '''
            SELECT date, SUM(amount) as total
            FROM expenses
            WHERE date >= ? AND date <= ?
            GROUP BY date
            ORDER BY date ASC
        '''
        
        df = pd.read_sql_query(query, conn, params=[start_date, end_date])
        conn.close()
        return df
