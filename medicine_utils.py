"""Helpers for medicine alternatives and price estimation."""
import re
from typing import List, Dict, Any
import pandas as pd
import numpy as np

def normalize_medicine_name(name: str) -> str:
    """Normalize medicine name for comparison."""
    return re.sub(r'[^a-z0-9]', '', name.lower())

def estimate_price_range(medicine_type: str, strength: str = None) -> tuple:
    """Estimate price range based on medicine type and strength."""
    # Base prices by medicine category (in ₹)
    base_prices = {
        'Antibiotics': (100, 500),
        'Antifungal': (80, 400),
        'Antihistamines': (50, 200),
        'Pain relievers': (30, 150),
        'Insulin': (500, 2000),
        'Corticosteroids': (150, 600),
        'Generic': (40, 200)
    }
    
    # Adjust for strength if provided
    if strength:
        try:
            value = float(re.search(r'(\d+)', strength).group(1))
            multiplier = 1 + (value / 100)  # Simple scaling based on strength
            return (
                round(base_prices.get(medicine_type, (50, 250))[0] * multiplier, 2),
                round(base_prices.get(medicine_type, (50, 250))[1] * multiplier, 2)
            )
        except (AttributeError, ValueError):
            pass
    
    return base_prices.get(medicine_type, (50, 250))

def categorize_medicine(name: str) -> str:
    """Categorize medicine by type based on name and common patterns."""
    name_lower = name.lower()
    
    categories = {
        'Antibiotics': ['cin', 'mycin', 'cillin', 'floxacin'],
        'Antifungal': ['conazole', 'fungal'],
        'Antihistamines': ['histamine', 'allergic'],
        'Pain relievers': ['pain', 'algic', 'gesic'],
        'Insulin': ['insulin'],
        'Corticosteroids': ['steroid', 'cort', 'sone']
    }
    
    for category, patterns in categories.items():
        if any(p in name_lower for p in patterns):
            return category
    
    return 'Generic'

def extract_strength(name: str) -> str:
    """Extract medicine strength from name."""
    match = re.search(r'(\d+(?:\.\d+)?(?:mg|g|ml|%|mcg))', name, re.IGNORECASE)
    return match.group(1) if match else None

def get_medicine_alternatives(query: str, medications_df: pd.DataFrame, max_results: int = 5) -> List[Dict[str, Any]]:
    """Find medicine alternatives with price estimates.
    
    Args:
        query: Medicine name to search for
        medications_df: DataFrame containing medicine data
        max_results: Maximum number of alternatives to return
    
    Returns:
        List of dicts containing alternative medicines with prices and savings
    """
    query_norm = normalize_medicine_name(query)
    
    # Extract medicine category and strength from query
    query_category = categorize_medicine(query)
    query_strength = extract_strength(query)
    
    # Get base price estimate for query
    query_price_range = estimate_price_range(query_category, query_strength)
    query_price = (query_price_range[0] + query_price_range[1]) / 2
    
    results = []
    seen = set()
    
    # Helper to process each medicine
    def process_medicine(med_name: str, disease: str = None) -> Dict[str, Any]:
        if not med_name or normalize_medicine_name(med_name) in seen:
            return None
            
        med_category = categorize_medicine(med_name)
        med_strength = extract_strength(med_name)
        price_range = estimate_price_range(med_category, med_strength)
        price = (price_range[0] + price_range[1]) / 2
        
        # Calculate potential savings
        savings = round(((query_price - price) / query_price) * 100) if price < query_price else 0
        
        seen.add(normalize_medicine_name(med_name))
        
        result = {
            'name': med_name,
            'price': price,
            'savings': savings if savings > 0 else None,
            'description': f"{med_category} medication" + (f" ({med_strength})" if med_strength else "")
        }
        
        if disease:
            result['description'] = f"Used for {disease}. " + result['description']
        
        if med_category != query_category:
            result['warning'] = f"This is a different type of medication ({med_category} vs {query_category}). Consult a healthcare provider before switching."
            
        return result
    
    # 1. Direct matches from medication lists
    for idx, row in medications_df.iterrows():
        try:
            med_list = eval(row['Medication']) if isinstance(row['Medication'], str) else row['Medication']
            if isinstance(med_list, (list, tuple)):
                for med in med_list:
                    if med and isinstance(med, str):
                        result = process_medicine(med.strip(), row.get('Disease'))
                        if result:
                            results.append(result)
        except:
            continue
    
    # Sort by savings (highest first) and similarity to query
    results.sort(key=lambda x: (
        x['savings'] if x['savings'] else 0,
        -len(set(normalize_medicine_name(x['name'])) ^ set(query_norm))
    ), reverse=True)
    
    return results[:max_results]