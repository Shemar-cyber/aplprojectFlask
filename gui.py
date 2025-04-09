import tkinter as tk
from tkinter import scrolledtext
import os
from command_processing import process_command, generate_ast
from lexer_parser import parser
from database import initialize_db
from config import show_help

def main():
    """
    Main entry point for the Ticket Booking System GUI application.
    Initializes the database and creates the graphical user interface.
    """
    try:
        # Initialize database connection and schema
        initialize_db()
    except Exception as e:
        print(f"There has been a fatal error: {str(e)}")
        return

    def run_function():
        """
        Handler for the Run button click event.
        Processes the user's command input and displays results.
        """
        input_entered = input_text_box.get("1.0", tk.END).strip()  
        if input_entered:
            try:
                # Parse and process the command
                result = parser.parse(input_entered.lower())
                process_command(input_entered, result, output_text_box)  
            except Exception as e:
                output_text_box.insert(tk.END, f"Error: {str(e)}\n")
        else:
            output_text_box.insert(tk.END, "Error: You did not enter a command.\n")

    def show_ast():
        input_entered = input_text_box.get("1.0", tk.END).strip()
        if input_entered:
            try:
                result = parser.parse(input_entered.lower())
                ast_image = generate_ast(result)  # AST generated ONLY here
                os.system(f"start {ast_image}")  # Windows
                # For Mac/Linux: use `open` or `xdg-open`
            except Exception as e:
                output_text_box.insert(tk.END, f"Error generating AST: {str(e)}\n")
        else:
            output_text_box.insert(tk.END, "Error: No command to generate AST from\n")

    
    # Initialize main application window
    gui_window = tk.Tk()
    gui_window.title("APBL Version 1.0 - Ticket Booking System")
    gui_window.geometry("800x700")
    gui_window.configure(bg="lightblue") 

    # Welcome label
    welcome_label = tk.Label(
        gui_window, 
        text="Welcome to the APBL Version 1.0 - Ticket Booking System!", 
        font=("Arial", 15, "bold"), 
        fg="Green", 
        bg="lightblue"
    )
    welcome_label.pack(padx=10, pady=15)

    # System guide section
    instructions_label = tk.Label(
        gui_window, 
        text="System Guide:", 
        font=(7), 
        bg="lightblue"
    )
    instructions_label.pack(padx=10, pady=15)
    
    instructions_text_box = scrolledtext.ScrolledText(
        gui_window,  
        wrap=tk.WORD, 
        height=7, 
        width=90
    )
    instructions_text_box.pack(padx=11, pady=6)
    instructions_text_box.insert(tk.END, show_help())  
    instructions_text_box.config(state=tk.DISABLED, bg="lightgrey") 

    # Command input section
    enter_command_label = tk.Label(
        gui_window, 
        text="Enter Command:", 
        font=(7), 
        bg="lightblue"
    )
    enter_command_label.pack(padx=10, pady=5)
    
    input_text_box = scrolledtext.ScrolledText(
        gui_window, 
        wrap=tk.WORD, 
        height=7, 
        width=90
    )
    input_text_box.pack(padx=11, pady=6)

    # Output display section
    output_label = tk.Label(
        gui_window, 
        text="Output:", 
        font=(9), 
        bg="lightblue"
    )
    output_label.pack(padx=10, pady=5)
    
    output_text_box = scrolledtext.ScrolledText(
        gui_window, 
        wrap=tk.WORD, 
        height=7, 
        width=90,
        bg="white"  # Better contrast for output
    )
    output_text_box.pack(padx=11, pady=6)

    # Button panel
    button_frame = tk.Frame(gui_window, bg="lightblue")
    button_frame.pack(pady=10)

    run_command_button = tk.Button(
        button_frame, 
        text="Run", 
        command=run_function, 
        font=(7), 
        bg="green", 
        fg="white", 
        relief="raised",
        padx=20  # Wider button for better click target
    )
    run_command_button.pack(side=tk.LEFT, padx=5)

    ast_button = tk.Button(
        button_frame, 
        text="Show AST", 
        command=show_ast, 
        font=(7), 
        bg="blue", 
        fg="white", 
        relief="raised",
        padx=20
    )
    ast_button.pack(side=tk.LEFT, padx=5)
    
    # Start the GUI event loop
    gui_window.mainloop()

if __name__ == '__main__':
    main()