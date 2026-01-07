import os
import sqlite3
import pickle
import base64
import hashlib
from flask import Flask, request, make_response, render_template_string

app = Flask(__name__)

# --- 1. SECRET SCANNING (CRITICAL/HIGH) ---
# Hardcoded credentials trigger secret scanning tools.
AWS_ACCESS_KEY = "AKIA5F7D3X9R2EXAMPLE" 
STRIPE_KEY = "sk_live_51MzXkL2eY6ghSjR8nK9pL2mN5qR8vWzX"
DATABASE_URL = "postgres://admin:password123@localhost:5432/mydb" # Hardcoded DB PW

@app.route("/vulnerable-complex")
def vulnerable_complex():
    # --- 2. SQL INJECTION (CRITICAL) ---
    user_id = request.args.get("id")
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # CodeQL: py/sql-injection
    query = "SELECT * FROM users WHERE id = '%s'" % user_id
    cursor.execute(query)

    # --- 3. INSECURE DESERIALIZATION (CRITICAL) ---
    # Accepting pickled data from users allows Remote Code Execution (RCE)
    data = request.args.get("data")
    if data:
        # CodeQL: py/unsafe-deserialization
        decoded_data = base64.b64decode(data)
        pickle.loads(decoded_data) 

    # --- 4. COMMAND INJECTION (HIGH) ---
    # User input flows directly into a system command
    filename = request.args.get("filename")
    # CodeQL: py/command-line-injection
    os.system("ls -l " + filename)

    # --- 5. PATH TRAVERSAL (HIGH) ---
    # CodeQL: py/path-injection
    with open(os.path.join("uploads", filename), "r") as f:
        content = f.read()

    # --- 6. CROSS-SITE SCRIPTING - XSS (MEDIUM) ---
    # Returning raw user input in HTML
    name = request.args.get("name", "Guest")
    # CodeQL: py/stack-trace-exposure & py/reflective-xss
    template = "<h1>Welcome %s</h1>" % name
    
    # --- 7. BROKEN CRYPTOGRAPHY (MEDIUM) ---
    # Using MD5 for "sensitive" hashing
    # CodeQL: py/weak-cryptographic-hash
    password = request.args.get("password")
    hashed_pw = hashlib.md5(password.encode()).hexdigest()

    # --- 8. INSECURE COOKIE SETTINGS (LOW/INFO) ---
    # CodeQL: py/cookie-missing-httponly
    response = make_response(render_template_string(template))
    response.set_cookie("session_id", "12345", httponly=False, secure=False)

    # --- 9. CLEAR-TEXT LOGGING (LOW) ---
    # Logging sensitive user info
    # CodeQL: py/clear-text-logging
    print(f"User {user_id} logged in with password {password}")

    return response

@app.route("/error")
def error_leak():
    # --- 10. INFORMATION EXPOSURE (LOW) ---
    # Returning full exception trace to the user
    try:
        1 / 0
    except Exception as e:
        # CodeQL: py/full-precision-money-leak
        return str(e), 500

if __name__ == "__main__":
    # --- 11. DEBUG MODE ENABLED (MEDIUM) ---
    # CodeQL: py/debug-mode-enabled
    app.run(debug=True, host="0.0.0.0")
