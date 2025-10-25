"""
Utilitaires de formatage de données pour l'application D-Tracker
"""

def format_currency(amount):
    """
    Formate un montant en devise
    
    Args:
        amount (float): Montant à formater
    
    Returns:
        str: Chaîne de caractères formatée en devise
    """
    return f"{amount:.2f} €"

def format_percentage(value):
    """
    Formate une valeur en pourcentage
    
    Args:
        value (float): Valeur à formater
    
    Returns:
        str: Chaîne de caractères formatée en pourcentage
    """
    return f"{value:+.1f}%"

def format_delta(value):
    """
    Formate une valeur delta avec le signe approprié
    
    Args:
        value (float): Valeur delta
    
    Returns:
        str: Chaîne de caractères delta formatée
    """
    return f"{value:+.2f}€"

def get_delta_class(value):
    """
    Obtient la classe CSS pour une valeur delta
    
    Args:
        value (float): Valeur delta
    
    Returns:
        str: Nom de la classe CSS
    """
    if value > 0:
        return "delta-positive"
    elif value < 0:
        return "delta-negative"
    else:
        return "delta-neutral"

