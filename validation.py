import datetime
from database import connect_db
from openai_integration import generate_ai_warning
from config import TICKET_LIMITS

def validate_datetime(date_str, time_str=None):
    """
    Validates date and time strings for correct format and future dates
    
    Args:
        date_str (str): Date string in YYYY-MM-DD format
        time_str (str, optional): Time string in HH:MM format
    
    Returns:
        str: Error message if validation fails, None if valid
    
    Validation Rules:
        1. Date must be in exact YYYY-MM-DD format
        2. Time (if provided) must be in exact HH:MM format
        3. Date must not be in the past
        4. Does not validate time against current time
    
    Examples:
        >>> validate_datetime("2025-12-31", "23:59")
        None  # Valid future datetime
        
        >>> validate_datetime("2020-01-01")
        "Date cannot be in the past"
    """
    try:
        # Parse and validate date
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        if date < datetime.date.today():
            return "Date cannot be in the past"
            
        # Parse time if provided (doesn't store it, just validates format)
        if time_str:
            datetime.datetime.strptime(time_str, "%H:%M")
            
        return None
    except ValueError as e:
        return f"Invalid format: {str(e)}. Use YYYY-MM-DD and HH:MM"

def check_ticket_limit(person, event_type, quantity=1):
    """
    Enforces per-person ticket limits using database checks and AI warnings
    
    Notes:
        - Limits are configured in config.TICKET_LIMITS
        - AI warning generates context-specific messages
    """
    conn = connect_db()
    cursor = conn.cursor()
    
    # Count existing active bookings for this person and event type
    cursor.execute('''
        SELECT COUNT(*) FROM bookings 
        WHERE resource = ? AND details LIKE ? AND status != 'Cancelled'
    ''', (event_type, f'%{person}%'))
    
    current_count = cursor.fetchone()[0]
    conn.close()
    
    # Check against configured limits
    limit = TICKET_LIMITS.get(event_type, 0)
    if current_count + quantity > limit:
        # Generate AI-powered warning message
        warning = generate_ai_warning(person, event_type, current_count, quantity)
        return False, warning
        
    return True, None