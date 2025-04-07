from database import *
from openai_integration import *
from validation import *
from lexer_parser import parser
from ast_generator import generate_ast
import tkinter as tk  # Add this import


def process_command(raw_command, parsed_command, output):
    """Process the parsed command and return a string to be rendered in Flask"""
    try:
        if not raw_command:
            output += "Error: Empty command\n"
            return output
            
        # Explain what the user is trying to do
        explanation = explain_user_command(raw_command)
        output += f"\nExplanation: {explanation}\n"
        
        if isinstance(parsed_command, str) and parsed_command.startswith("Error"):
            output += parsed_command + "\n"
            return output
            
        # Generate AST visualization
        ast_image = generate_ast(parsed_command)
        output += f"\nAST generated: {ast_image}\n"
        
        if parsed_command[0] == 'LIST':
            event_type = parsed_command[1]
            if event_type not in ['concert', 'football', 'train', 'airline']:
                output += "Error: Can only list concert, football, train, or airline tickets\n"
                return output
                
            output += get_real_time_info(event_type) + "\n"
            
        elif parsed_command[0] == 'BOOK':
            details = parsed_command[1]
            if 'person' not in details or not details['person']:
                output += "Error: Must specify a person for booking\n"
                return output
                
            if 'date' in details:
                error = validate_datetime(details['date'], details.get('time'))
                if error:
                    output += error + "\n"
                    return output
            
            # Check ticket limits
            event_type = details['type']
            person = details['person']
            within_limit, warning = check_ticket_limit(person, event_type)
            
            if not within_limit:
                output += f"WARNING: {warning}\n"
                return output
                   
            add_booking(event_type, details, "BOOK", "Reserved")
            output += f"Added booking for {person}\n"
                
        elif parsed_command[0] in ['CONFIRM', 'PAY', 'CANCEL']:
            action = parsed_command[0]
            data = parsed_command[1]
            
            if 'person' not in data or not data['person']:
                output += "Error: Must specify a person\n"
                return output
                
            update_booking_status(data['type'], data['person'], action.capitalize())
            output += f"Booking {action.lower()}ed for {data['person']}\n"
                
        elif parsed_command[0] == 'VIEW':
            output += "\nCurrent Bookings:\n"
            bookings = list_bookings()
            if not bookings:
                output += "No bookings found.\n"
            else:
                for booking in bookings:
                    output += f"ID: {booking[0]}, Resource: {booking[1]}, Details: {booking[3]}, Status: {booking[4]}\n"
        else:
            output += "Unrecognized command. Type 'help' for instructions.\n"
            
    except Exception as e:
        output += f"Error: {str(e)}\n"
    
    return output

