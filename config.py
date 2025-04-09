# Configuration and constants for the Ticket Booking System

# Ticket Limits Configuration
# --------------------------
# Defines maximum number of tickets allowed per person for each event type
# This acts as a system-wide constraint to prevent ticket hoarding
TICKET_LIMITS = {
    'concert': 4,    # Maximum 4 concert tickets per user (typically for high-demand events)
    'football': 6,   # Maximum 6 football tickets (slightly higher for group attendance)
    'train': 10,     # Maximum 10 train tickets (higher limit for transportation needs)
    'airline': 4     # Maximum 4 airline tickets (similar to concert for revenue management)
}

def show_help():
    """
    Returns formatted help text explaining system capabilities and usage rules.
    This serves as both user documentation and input validation reference.
    
    The help text includes:
    - Supported command syntax
    - Format requirements for dates/times
    - Name input handling
    - Ticket limit information (mirroring TICKET_LIMITS configuration)
    
    Returns:
        str: Multi-line help message string
    """
    return """SUPPORTED COMMANDS:
    - List [concert|football|train|airline] tickets in my area
    - Book train|airline from [location] to [location] on [date] at [time] for [name]
    - Book [event name] concert|football match for [name]
    - Confirm|Pay|Cancel [event type] for [name]
    - View bookings

GENERAL NOTES:
    - Dates must be in YYYY-MM-DD format (e.g., 2025-04-15)
    - Times must be in HH:MM 24-hour format (e.g., 14:30)
    - Names can be in quotes for multi-word names (e.g., "John Smith")
    - TICKET LIMITS
    Max 4 concert tickets per person
    Max 6 football tickets per person
    Max 10 train tickets per person
    Max 4 airline tickets per person"""

# Logging Configuration
# --------------------
# Sets up basic logging for the application with:
# - INFO level logging (captures operational messages)
# - Timestamped format for better traceability
# This configuration will affect all log messages throughout the application
import logging
logging.basicConfig(
    level=logging.INFO,  # Log level: INFO and above (INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log message format
)