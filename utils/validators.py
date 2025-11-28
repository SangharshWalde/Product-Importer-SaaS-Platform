import re
from typing import Optional


def validate_sku(sku: str) -> bool:
    """
    Validate SKU format
    
    Args:
        sku: SKU string to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not sku or len(sku) > 100:
        return False
    # SKU should contain only alphanumeric, hyphens, and underscores
    return bool(re.match(r'^[A-Za-z0-9_-]+$', sku))


def validate_price(price: float) -> bool:
    """
    Validate price value
    
    Args:
        price: Price to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        price_float = float(price)
        return price_float >= 0
    except (ValueError, TypeError):
        return False


def validate_quantity(quantity: int) -> bool:
    """
    Validate quantity value
    
    Args:
        quantity: Quantity to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        quantity_int = int(quantity)
        return quantity_int >= 0
    except (ValueError, TypeError):
        return False


def validate_url(url: str) -> bool:
    """
    Validate URL format for webhooks
    
    Args:
        url: URL to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not url:
        return False
    # Basic URL validation
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return bool(url_pattern.match(url))


def validate_csv_headers(headers: list) -> tuple[bool, Optional[str]]:
    """
    Validate CSV headers
    
    Args:
        headers: List of header names
        
    Returns:
        tuple: (is_valid, error_message)
    """
    required_headers = {'sku', 'name', 'price'}
    headers_lower = {h.lower().strip() for h in headers}
    
    missing = required_headers - headers_lower
    if missing:
        return False, f"Missing required headers: {', '.join(missing)}"
    
    return True, None
