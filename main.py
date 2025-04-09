
from flask import Flask, render_template, request, flash, redirect, url_for
from command_processing import process_command
from lexer_parser import parser
from database import initialize_db
from config import show_help
from ast_generator import generate_ast
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        command = request.form.get('command_input', '').strip()
        if command:
            try:
                result = parser.parse(command.lower())
                output = process_command(command, result, None)  # Pass None for output_box to get return value
                return render_template('index.html', command=command, output=output, help_text=show_help())
            except Exception as e:
                flash(str(e), 'error')
                return render_template('index.html', command=command, output='', help_text=show_help())
        else:
            flash('Error: You did not enter a command.', 'error')
    
    return render_template('index.html', command='', output='', help_text=show_help())

@app.route('/show_ast')
def show_ast_route():
    command = request.args.get('command_input', '').strip()
    if command:
        try:
            result = parser.parse(command.lower())
            ast_image = generate_ast(result)
            return redirect(url_for('static', filename=ast_image))
        except Exception as e:
            flash(f'Error generating AST: {str(e)}', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    try:
        initialize_db()
        app.run(host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"Fatal error: {str(e)}")
