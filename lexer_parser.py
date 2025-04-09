import ply.lex as lex
import ply.yacc as yacc

# --------------------------
# Lexer (Tokenizer)
# --------------------------

# Define all valid token types that the lexer can produce
tokens = (
    # Command verbs
    'LIST', 'BOOK', 'CONFIRM', 'PAY', 'CANCEL', 'VIEW',
    # Resource types
    'CONCERT', 'FOOTBALL', 'TRAIN', 'AIRLINE', 'TICKETS',
    # Prepositions and keywords
    'FROM', 'TO', 'ON', 'AT', 'FOR', 'IN', 'MY', 'AREA', 'MATCH',
    # Data types
    'DATE', 'TIME', 'STRING', 'BOOKINGS', 'IDENTIFIER'
)

# Token matching rules (all case-insensitive)
# Each function defines a regular expression pattern to match a token

def t_LIST(t):
    r'[Ll][Ii][Ss][Tt]'  # Matches "list" in any case combination
    return t

def t_BOOKINGS(t):
    r'[Bb][Oo][Oo][Kk][Ii][Nn][Gg][Ss]'  # Matches "bookings"
    return t

def t_BOOK(t):
    r'[Bb][Oo][Oo][Kk]'  # Matches "book"
    return t

def t_CONFIRM(t):
    r'[Cc][Oo][Nn][Ff][Ii][Rr][Mm]'  # Matches "confirm"
    return t

def t_PAY(t):
    r'[Pp][Aa][Yy]'  # Matches "pay"
    return t

def t_CANCEL(t):
    r'[Cc][Aa][Nn][Cc][Ee][Ll]'  # Matches "cancel"
    return t

def t_VIEW(t):
    r'[Vv][Ii][Ee][Ww]'  # Matches "view"
    return t

# Resource type tokens
def t_CONCERT(t):
    r'[Cc][Oo][Nn][Cc][Ee][Rr][Tt]'  # Matches "concert"
    return t

def t_FOOTBALL(t):
    r'[Ff][Oo][Oo][Tt][Bb][Aa][Ll][Ll]'  # Matches "football"
    return t

def t_TRAIN(t):
    r'[Tt][Rr][Aa][Ii][Nn]'  # Matches "train"
    return t

def t_AIRLINE(t):
    r'[Aa][Ii][Rr][Ll][Ii][Nn][Ee]'  # Matches "airline"
    return t

def t_TICKETS(t):
    r'[Tt][Ii][Cc][Kk][Ee][Tt][Ss]'  # Matches "tickets"
    return t

def t_MATCH(t):
    r'[Mm][Aa][Tt][Cc][Hh]'  # Matches "match"
    return t

# Preposition tokens
def t_FROM(t):
    r'[Ff][Rr][Oo][Mm]'  # Matches "from"
    return t

def t_TO(t):
    r'[Tt][Oo]'  # Matches "to"
    return t

def t_ON(t):
    r'[Oo][Nn]'  # Matches "on"
    return t

def t_AT(t):
    r'[Aa][Tt]'  # Matches "at"
    return t

def t_FOR(t):
    r'[Ff][Oo][Rr]'  # Matches "for"
    return t

def t_IN(t):
    r'[Ii][Nn]'  # Matches "in"
    return t

def t_MY(t):
    r'[Mm][Yy]'  # Matches "my"
    return t

def t_AREA(t):
    r'[Aa][Rr][Ee][Aa]'  # Matches "area"
    return t

# Data type tokens
def t_DATE(t):
    r'\d{4}-\d{2}-\d{2}'  # Matches YYYY-MM-DD format
    return t

def t_TIME(t):
    r'\d{2}:\d{2}'  # Matches HH:MM 24-hour format
    return t

def t_STRING(t):
    r'\"[^\"]+\"'  # Matches quoted strings like "John Doe"
    t.value = t.value.strip('\"')  # Remove quotes from value
    return t

def t_IDENTIFIER(t):
    r'[A-Za-z]+'  # Matches any word not caught by other rules
    t.value = t.value.lower()  # Convert to lowercase for consistency
    return t

# Ignore whitespace and tabs
t_ignore = ' \t'

def t_error(t):
    """Error handling for invalid characters"""
    error_msg = f"Invalid character '{t.value[0]}'"
    t.lexer.skip(1)  # Skip the offending character
    return error_msg

# Build the lexer
lexer = lex.lex()

# --------------------------
# Parser Rules (Grammar Rules)
# --------------------------
def p_statement(p):
    """statement : list_command
                 | booking_command
                 | status_command
                 | view_command"""
    p[0] = p[1] # Return the parse commands

def p_list_command(p): 
    """list_command : LIST event_type TICKETS IN MY AREA"""
    p[0] = ('LIST', p[2].lower()) # Returns tuple (command, event_type)

def p_booking_command(p):
    """booking_command : book_transport
                      | book_event"""
    p[0] = p[1]

def p_book_transport(p):
    """book_transport : BOOK TRAIN FROM location TO location ON DATE AT TIME FOR person
                     | BOOK AIRLINE FROM location TO location ON DATE AT TIME FOR person"""
    p[0] = ('BOOK', {
        'type': p[2].lower(), # 'train' or 'airline'
        'from': ' '.join(p[4]),  # Joined location parts
        'to': ' '.join(p[6]), # Joined destination parts
        'date': p[8], # Date string
        'time': p[10], # Time string
        'person': ' '.join(p[12]) # Person's name
    })

def p_book_event(p):
    """book_event : BOOK event_name CONCERT FOR person
                 | BOOK event_name FOOTBALL MATCH FOR person"""
    p[0] = ('BOOK', {
        'type': p[3].lower(),
        'name': ' '.join(p[2]),  # Event type
        'person': ' '.join(p[5]) if p[3].lower() == 'concert' else ' '.join(p[6])
    })

def p_status_command(p):
    """status_command : CONFIRM event_type FOR person
                      | PAY event_type FOR person
                      | CANCEL event_type FOR person"""
    p[0] = (p[1].upper(), { # Action in uppercase
        'type': p[2],  # Event type
        'person': ' '.join(p[4])
    })

def p_view_command(p):
    """view_command : VIEW BOOKINGS"""
    p[0] = ('VIEW', {'action': 'show_bookings'})

# Helper rules for complex grammar elements
def p_event_type(p):
    """event_type : CONCERT
                 | FOOTBALL
                 | TRAIN
                 | AIRLINE"""
    p[0] = p[1].lower() # Return lowercase version

def p_location(p):
    """location : IDENTIFIER
               | STRING
               | location IDENTIFIER"""
    if len(p) == 2:
        p[0] = [p[1]] # Single word location
    else:
        p[0] = p[1] + [p[2]] # Multi-word location

def p_person(p):
    """person : IDENTIFIER
             | STRING
             | person IDENTIFIER"""
    if len(p) == 2:
        p[0] = [p[1]] # Single word name
    else:
        p[0] = p[1] + [p[2]] # Multi-word name

def p_event_name(p):
    """event_name : IDENTIFIER
                 | STRING
                 | event_name IDENTIFIER"""
    if len(p) == 2:
        p[0] = [p[1]] # Single word event name
    else:
        p[0] = p[1] + [p[2]] # Multi-word event name

def p_error(p):
    if p:
        error_msg = f"Syntax error at '{p.value}'"
    else:
        error_msg = "Syntax error at end of input"
    return error_msg

#Build the parser
parser = yacc.yacc()