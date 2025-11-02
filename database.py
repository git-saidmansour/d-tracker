import sqlite3
import pandas as pd
from datetime import datetime
import os

class ExpenseDatabase:
    def __init__(self, db_path="expenses.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialise la base de données avec les tables nécessaires."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Activer les clés étrangères
        cursor.execute('PRAGMA foreign_keys = ON;')
        
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

        # 👉 N'insérer les catégories par défaut QUE si la table est vide
        cursor.execute('SELECT COUNT(*) FROM categories;')
        nb = cursor.fetchone()[0] or 0
        if nb == 0:
            cursor.executemany(
                'INSERT INTO categories (name, color) VALUES (?, ?)',
                self._default_categories()
            )
        
        conn.commit()
        conn.close()

    # --------------------------- EXPENSES ---------------------------
    def add_expense(self, amount, description, category_id, date):
        """Ajoute une nouvelle dépense."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')

        cursor.execute(
            'INSERT INTO expenses (amount, description, category_id, date) VALUES (?, ?, ?, ?)',
            (amount, description, category_id, date)
        )
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id

    def get_expenses(self, start_date=None, end_date=None, category_name=None):
        """
        Récupère les dépenses.
        NOTE: les paramètres de période sont ignorés (filtre date supprimé).
        """
        conn = sqlite3.connect(self.db_path)
        query = '''
            SELECT 
                e.id,
                e.amount,
                e.description,
                e.date,
                c.name AS category,
                c.color
            FROM expenses e
            LEFT JOIN categories c ON e.category_id = c.id
            WHERE 1=1
        '''
        params = []

        # Filtre catégorie (optionnel, insensible à la casse)
        if category_name:
            query += " AND LOWER(c.name) = LOWER(?)"
            params.append(str(category_name))

        # Tri du plus récent au plus ancien
        query += " ORDER BY e.date DESC"

        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df

    def get_total_expenses(self, start_date=None, end_date=None):
        """
        Calcule le total des dépenses.
        NOTE: les paramètres de période sont ignorés (filtre date supprimé).
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT SUM(amount) FROM expenses')
        total = cursor.fetchone()[0] or 0
        conn.close()
        return total

    # --------------------------- CATEGORIES ---------------------------
    def add_category(self, name, color):
        """Ajoute une nouvelle catégorie."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')

        cursor.execute(
            'INSERT INTO categories (name, color) VALUES (?, ?)',
            (name.strip(), color.strip())
        )
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id
    
    def get_categories(self):
        """Récupère toutes les catégories."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, color FROM categories ORDER BY name')
        categories = cursor.fetchall()
        conn.close()
        return categories

    def get_category_by_name(self, name):
        """Récupère une catégorie par son nom."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT id, name, color FROM categories WHERE LOWER(name) = LOWER(?)',
            (name.strip(),)
        )
        row = cursor.fetchone()
        conn.close()
        return row

    def get_expense_count_by_category(self, category_id):
        """Retourne le nombre de dépenses liées à une catégorie."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM expenses WHERE category_id = ?', (category_id,))
        count = cursor.fetchone()[0] or 0
        conn.close()
        return count

    def reassign_expenses(self, from_category_id, to_category_id):
        """Réassigne toutes les dépenses d'une catégorie source vers une autre."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE expenses SET category_id = ? WHERE category_id = ?',
            (to_category_id, from_category_id)
        )
        conn.commit()
        conn.close()

    def merge_categories(self, source_category_id, target_category_id, new_name=None, new_color=None):
        """Fusionne deux catégories (réassignation + suppression de la source)."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(
                'UPDATE expenses SET category_id = ? WHERE category_id = ?',
                (target_category_id, source_category_id)
            )
            if new_name or new_color:
                cursor.execute('SELECT name, color FROM categories WHERE id = ?', (target_category_id,))
                cur = cursor.fetchone()
                if cur:
                    cur_name, cur_color = cur
                    final_name = new_name if new_name else cur_name
                    final_color = new_color if new_color else cur_color
                    cursor.execute(
                        'UPDATE categories SET name = ?, color = ? WHERE id = ?',
                        (final_name, final_color, target_category_id)
                    )
            cursor.execute('DELETE FROM categories WHERE id = ?', (source_category_id,))
            conn.commit()
            return True, "Catégories fusionnées"
        except Exception as e:
            conn.rollback()
            return False, f"Erreur de fusion : {e}"
        finally:
            conn.close()

    def update_category(self, category_id, name, color):
        """Met à jour une catégorie ou fusionne si le nom existe déjà."""
        name = name.strip()
        color = color.strip()
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(
                'UPDATE categories SET name = ?, color = ? WHERE id = ?',
                (name, color, category_id)
            )
            conn.commit()
            if cursor.rowcount > 0:
                conn.close()
                return True, "Catégorie mise à jour"
            conn.close()
            return False, "Aucune catégorie trouvée."
        except sqlite3.IntegrityError:
            conn.close()
            target = self.get_category_by_name(name)
            if target:
                target_id, _, target_color = target
                ok, msg = self.merge_categories(category_id, target_id, name, color or target_color)
                return (True, "Catégories fusionnées") if ok else (False, msg)
            return False, "Erreur d'intégrité : nom déjà pris."
        except Exception as e:
            conn.close()
            return False, f"Erreur : {e}"

    def delete_category(self, category_id):
        """Supprime une catégorie si aucune dépense n'y est associée."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM expenses WHERE category_id = ?', (category_id,))
        count = cursor.fetchone()[0] or 0
        if count > 0:
            conn.close()
            return False, f"Il y a {count} dépense(s) associée(s)."
        cursor.execute('DELETE FROM categories WHERE id = ?', (category_id,))
        conn.commit()
        conn.close()
        return True, "Catégorie supprimée"

    def delete_category_reassign(self, source_category_id, target_category_id):
        """Réassigne les dépenses puis supprime la catégorie source."""
        if source_category_id == target_category_id:
            return False, "La catégorie cible doit être différente."
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(
                'UPDATE expenses SET category_id = ? WHERE category_id = ?',
                (target_category_id, source_category_id)
            )
            cursor.execute('DELETE FROM categories WHERE id = ?', (source_category_id,))
            conn.commit()
            return True, "Dépenses réassignées et catégorie supprimée"
        except Exception as e:
            conn.rollback()
            return False, f"Erreur : {e}"
        finally:
            conn.close()

    # ---------- Restauration des catégories par défaut ----------
    def _default_categories(self):
        """Liste interne des catégories par défaut."""
        return [
            ('Alimentation', '#ff7f0e'),
            ('Transport',   '#2ca02c'),
            ('Logement',    '#d62728'),
            ('Santé',       '#9467bd'),
            ('Loisirs',     '#8c564b'),
            ('Shopping',    '#e377c2'),
            ('Éducation',   '#7f7f7f'),
            ('Autres',      '#bcbd22')
        ]

    def ensure_default_categories(self):
        """
        Réinsère les catégories par défaut manquantes (INSERT OR IGNORE).
        Ne touche pas aux catégories existantes ni aux dépenses.
        """
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.executemany(
            'INSERT OR IGNORE INTO categories(name, color) VALUES(?, ?)',
            self._default_categories()
        )
        conn.commit()
        conn.close()
        return True, "Catégories par défaut restaurées (ajout des manquantes uniquement)"
