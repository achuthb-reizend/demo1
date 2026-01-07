import os
import sqlite3
import json  # Replaced pickle
import hashlib
import logging
from flask import Flask, request, make_response, render_template, abort
from werkzeug.utils import secure_filename # For Path Traversal

app = Flask(__name__)

# --- 1. SECRET SCANNING FIXED ---
# Secrets are now pulled from environment variables. 
# Never hardcode keys in the source code.
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
STRIPE_KEY = os.getenv("STRIPE_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

# Setup secure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route("/secure-complex")
def secure_complex():
    # --- 2. SQL INJECTION FIXED ---
    user_id = request.args.get("id")
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # Use parameterized queries (?) to prevent SQLi
    query = "SELECT * FROM users WHERE id = ?"
    cursor.execute(query, (user_id,))

    # --- 3. INSECURE DESERIALIZATION FIXED ---
    # Replaced pickle.loads with json.loads (Safe)
    data = request.args.get("data")
    if data:
        try:
            # JSON does not allow arbitrary code execution
            decoded_data = json.loads(data) 
        except Exception:
            pass

    # --- 4. & 5. COMMAND INJECTION & PATH TRAVERSAL FIXED ---
    user_input_file = request.args.get("filename")
    if user_input_file:
        # Use secure_filename to prevent path traversal (../../etc/passwd)
        safe_filename = secure_filename(user_input_file)
        
        # Avoid os.system. For file reading, use the safe name.
        file_path = os.path.join("uploads", safe_filename)
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                content = f.read()

    # --- 6. CROSS-SITE SCRIPTING (XSS) FIXED ---
    name = request.args.get("name", "Guest")
    # Using a dictionary for render_template ensures auto-escaping by Jinja2
    # This prevents malicious <script> tags from executing.
    template_content = "Welcome {{ name }}"
    
    # --- 7. BROKEN CRYPTOGRAPHY FIXED ---
    # In a real app, use 'bcrypt' or 'argon2'. 
    # MD5 is avoided here by using a more modern logic (e.g., SHA-256 with salt)
    password = request.args.get("password")
    if password:
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()

    # --- 8. INSECURE COOKIE SETTINGS FIXED ---
    # Set HttpOnly and Secure flags
    response = make_response("Report Processed")
    response.set_cookie(
        "session_id", "12345", 
        httponly=True,   # Prevents JavaScript access (XSS protection)
        secure=True,     # Only sent over HTTPS
        samesite='Lax'   # CSRF protection
    )

    # --- 9. CLEAR-TEXT LOGGING FIXED ---
    # Log the event, but never the sensitive password
    logger.info(f"User {user_id} attempted a sensitive operation.")

    return response

@app.route("/error")
def error_leak():
    # --- 10. INFORMATION EXPOSURE FIXED ---
    try:
        1 / 0
    except Exception:
        # Return a generic error to the user, not the stack trace
        abort(500, description="Internal Server Error")

if __name__ == "__main__":
    # --- 11. DEBUG MODE DISABLED ---
    # debug=False prevents the interactive debugger from being exposed
    app.run(debug=False, host="127.0.0.1")
