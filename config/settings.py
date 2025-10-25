"""
Paramètres de configuration pour l'application D-Tracker
"""

# Configuration de la page Streamlit
PAGE_CONFIG = {
    "page_title": "D-Tracker",
    "page_icon": "💰",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Styles CSS
CSS_STYLES = """
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    .progress-container {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    .category-name {
        font-weight: bold;
        color: #333;
        margin-bottom: 0.5rem;
    }
    .progress-bar {
        background-color: #e9ecef;
        border-radius: 10px;
        height: 20px;
        overflow: hidden;
    }
    .progress-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 0.3s ease;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    .delta-positive {
        color: #dc3545;
    }
    .delta-negative {
        color: #28a745;
    }
    .delta-neutral {
        color: #6c757d;
    }
    .nav-button {
        margin: 0.5rem 0;
        border-radius: 10px;
        font-weight: 500;
    }
    .nav-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
</style>
"""

# Catégories par défaut
DEFAULT_CATEGORIES = [
    ('Alimentation', '#ff7f0e'),
    ('Transport', '#2ca02c'),
    ('Logement', '#d62728'),
    ('Santé', '#9467bd'),
    ('Loisirs', '#8c564b'),
    ('Shopping', '#e377c2'),
    ('Éducation', '#7f7f7f'),
    ('Autres', '#bcbd22')
]

