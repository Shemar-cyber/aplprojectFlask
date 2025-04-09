from database import *
from openai_integration import *
from validation import *
from lexer_parser import parser
from ast_generator import generate_ast
import tkinter as tk  # GUI toolkit for output display

def process_command(raw_command, parsed_command, output_box=None):
    """
    Main command processing pipeline that handles the complete workflow from
    raw input to system response. Integrates all system components.

    Args:
        raw_command (str): Original user input string
        parsed_command (tuple/str): Structured output from parser or error string
        output_box (Optional[tk.scrolledtext]): GUI text widget for displaying results
    
    Workflow:
        1. Input validation
        2. Natural language explanation
        3. AST generation
        4. Command-specific processing
        5. Database operations
        6. Output display
    """
    try:
        # Input validation
        if not raw_command:
            message = "Error: Empty command\n"
            if output_box:
                output_box.insert(tk.END, message)
                return
            return message
            
        # Generate natural language explanation using AI
        explanation = explain_user_command(raw_command)
        output = f"\nExplanation: {explanation}\n"
        if output_box:
            output_box.insert(tk.END, output)
        
        # Handle parser errors
        if isinstance(parsed_command, str) and parsed_command.startswith("Error"):
            error_msg = parsed_command + "\n"
            if output_box:
                output_box.insert(tk.END, error_msg)
                return
            return output + error_msg
            
        # Generate and display abstract syntax tree visualization
        #ast_image = generate_ast(parsed_command)
        #output_box.insert(tk.END, f"\nAST generated: {ast_image}\n")
        
        # Command routing
        command_type = parsed_command[0]
        
        if command_type == 'LIST':
            result = _handle_list_command(parsed_command, output_box)
            
        elif command_type == 'BOOK':
            result = _handle_book_command(parsed_command, output_box)
                
        elif command_type in ['CONFIRM', 'PAY', 'CANCEL']:
            result = _handle_status_command(parsed_command, output_box)
                
        elif command_type == 'VIEW':
            result = _handle_view_command(output_box)
            
        else:
            result = "Unrecognized command. Type 'help' for instructions.\n"
            if output_box:
                output_box.insert(tk.END, result)
            else:
                return output + result
        
        # Return combined output if not using output_box
        if not output_box:
            return output + result
            
    except Exception as e:
        error_msg = f"System Error: {str(e)}\n"
        if output_box:
            output_box.insert(tk.END, error_msg)
        else:
            return output + error_msg if 'output' in locals() else error_msg

# --------------------------
# Command Handler Functions
# --------------------------

def _handle_list_command(parsed_command, output_box):
    """
    Processes LIST commands to show available events/tickets
    """
    event_type = parsed_command[1]
    valid_events = ['concert', 'football', 'train', 'airline']
    
    if event_type not in valid_events:
        message = f"Error: Can only list {', '.join(valid_events)} tickets\n"
        if output_box:
            output_box.insert(tk.END, message)
        return message
        
    # Get real-time event information from external source
    event_info = get_real_time_info(event_type)
    if output_box:
        output_box.insert(tk.END, event_info + "\n")
    return event_info + "\n"

def _handle_book_command(parsed_command, output_box):
    """
    Processes BOOK commands with validation and database operations
    """
    details = parsed_command[1]
    
    # Person validation
    if 'person' not in details or not details['person']:
        message = "Error: Must specify a person for booking\n"
        if output_box:
            output_box.insert(tk.END, message)
        return message
        
    # Date/time validation
    if 'date' in details:
        error = validate_datetime(details['date'], details.get('time'))
        if error:
            if output_box:
                output_box.insert(tk.END, error + "\n")
            return error + "\n"
    
    # Ticket limit enforcement
    event_type = details['type']
    person = details['person']
    within_limit, warning = check_ticket_limit(person, event_type)
    
    if not within_limit:
        message = f"WARNING: {warning}\n"
        if output_box:
            output_box.insert(tk.END, message)
        return message
            
    # Database operation
    add_booking(event_type, details, "BOOK", "Reserved")
    message = f"Added booking for {person}\n"
    if output_box:
        output_box.insert(tk.END, message)
    return message

def _handle_status_command(parsed_command, output_box):
    """
    Processes status change commands (CONFIRM/PAY/CANCEL)
    """
    action = parsed_command[0]
    data = parsed_command[1]
    
    if 'person' not in data or not data['person']:
        message = "Error: Must specify a person\n"
        if output_box:
            output_box.insert(tk.END, message)
        return message
        
    update_booking_status(data['type'], data['person'], action.capitalize())
    message = f"Booking {action.lower()}ed for {data['person']}\n"
    if output_box:
        output_box.insert(tk.END, message)
    return message

def _handle_view_command(output_box):
    """
    Processes VIEW BOOKINGS command to display all reservations
    """
    message = "\nCurrent Bookings:\n"
    if output_box:
        output_box.insert(tk.END, message)
    else:
        output = message
        
    bookings = list_bookings()
    
    if not bookings:
        message = "No bookings found.\n"
        if output_box:
            output_box.insert(tk.END, message)
        return message
    else:
        for booking in bookings:
            message = (
                f"ID: {booking[0]}, "
                f"Resource: {booking[1]}, "
                f"Details: {booking[3]}, "
                f"Status: {booking[4]}\n"
            )
            if output_box:
                output_box.insert(tk.END, message)
            else:
                output += message
        return output if not output_box else None