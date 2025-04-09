import sqlite3
import datetime

def connect_db():
    """
    Establishes connection to SQLite database file
    
    Returns:
        sqlite3.Connection: Database connection object
    
    Notes:
        - Uses SQLite's built-in connection pooling
        - Creates bookings.db file if it doesn't exist
        - Default isolation level is DEFERRED
    """
    return sqlite3.connect('bookings.db')

def initialize_db():
    """
    Creates the database schema if it doesn't exist
    
    Schema Details:
        - id: Auto-incrementing primary key
        - resource: Type of booking (concert/football/train/airline)
        - action: Booking action (BOOK/CONFIRM/PAY/CANCEL)
        - details: JSON-like string of booking particulars
        - status: Current status (Reserved/Confirmed/Paid/Cancelled)
        - timestamp: ISO format datetime of record creation/modification
    
    Notes:
        - Uses IF NOT EXISTS to prevent errors on multiple calls
        - Commits changes immediately after execution
        - Always closes connection to prevent leaks
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        resource TEXT,
        action TEXT,
        details TEXT,
        status TEXT,
        timestamp TEXT
    )''')
    conn.commit()
    conn.close()

def add_booking(resource, details, action, status):
    """
    Inserts a new booking record
    
    Args:
        resource (str): Type of resource being booked
        details (dict/str): Booking particulars (converted to string)
        action (str): Action performed (BOOK/CONFIRM/etc)
        status (str): Initial status of booking
    
    Process Flow:
        1. Creates timestamp in ISO format
        2. Converts details to string representation
        3. Uses parameterized query to prevent SQL injection
        4. Commits transaction immediately
    
    Security:
        - Uses parameterized queries exclusively
        - Automatic connection cleanup
    """
    conn = connect_db()
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().isoformat()
    cursor.execute('''
        INSERT INTO bookings 
        (resource, action, details, status, timestamp) 
        VALUES (?, ?, ?, ?, ?)''',
        (resource, action, str(details), status, timestamp))
    conn.commit()
    conn.close()

def update_booking_status(resource, person, new_status):
    """
    Updates the most recent booking matching criteria
    
    Args:
        resource (str): Type of resource to update
        person (str): Name to match in details
        new_status (str): New status to set
    
    Query Logic:
        - Uses subquery to find most recent matching booking
        - LIKE operator for name matching in details text
        - Updates both status and modification timestamp
        - Limits to one record with DESC/LIMIT 1
    
    Notes:
        - % wildcards in LIKE pattern match any text around the name
        - ISO timestamp provides sortable chronological record
    """
    conn = connect_db()
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().isoformat()
    cursor.execute('''
        UPDATE bookings 
        SET status = ?, timestamp = ? 
        WHERE id = (
            SELECT id FROM bookings 
            WHERE resource = ? AND details LIKE ? 
            ORDER BY id DESC LIMIT 1
        )''', 
        (new_status, timestamp, resource, f'%{person}%'))
    conn.commit()
    conn.close()

def list_bookings():
    """
    Retrieves all booking records
    
    Returns:
        list: All rows from bookings table
    
    Data Structure:
        Each row contains:
        - id (int)
        - resource (str)
        - action (str)
        - details (str)
        - status (str)
        - timestamp (str)
    
    Notes:
        - Returns raw result set for flexibility
        - Caller must handle result processing
        - Empty list returned if no bookings exist
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bookings')
    bookings = cursor.fetchall()
    conn.close()
    return bookings