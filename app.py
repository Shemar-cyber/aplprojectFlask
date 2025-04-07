from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from command_processing import process_command, generate_ast
from lexer_parser import parser
from database import initialize_db
from config import show_help

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for flashing messages

# Initialize database with error handling
db = None
try:
    db = initialize_db()
    if db is None:
        print("Warning: Database initialization returned None")
except Exception as e:
    print(f"Fatal error initializing DB: {e}")

@app.route("/", methods=["GET", "POST"])
def index():
    output = ""
    command = ""

    if request.method == "POST":
        command = request.form.get("command_input", "").strip()
        if command:
            try:
                result = parser.parse(command.lower())
                output = process_command(command, result, output)  # Pass output as a string
            except Exception as e:
                output = f"Error: {str(e)}"
                print(f"Detailed error: {e}")  # For debugging
        else:
            flash("You did not enter a command.", "error")

    return render_template("index.html", help_text=show_help(), output=output, command=command)

@app.route("/show_ast", methods=["POST"])
def show_ast_route():
    command = request.form.get("command_input", "").strip()
    if command:
        try:
            result = parser.parse(command.lower())
            ast_path = generate_ast(result)
            return send_file(ast_path, mimetype='image/png')
        except Exception as e:
            flash(f"Error generating AST: {str(e)}", "error")
    else:
        flash("No command to generate AST from.", "error")

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
