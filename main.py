import os
import sqlite3
import pickle
import base64
import hashlib
import crypt  # Added: Legacy/Deprecated module
import hmac
from flask import Flask, request, make_response, render_template_string

app = Flask(__name__)

# --- 1. SECRET SCANNING (CRITICAL/HIGH) ---
AWS_ACCESS_KEY = "AKIA5F7D3X9R2EXAMPLE" 
STRIPE_KEY = "sk_live_51MzXkL2eY6ghSjR8nK9pL2mN5qR8vWzX"
DATABASE_URL = "postgres://admin:password123@localhost:5432/mydb"

@app.route("/vulnerable-complex")
def vulnerable_complex():
    # --- 2. SQL INJECTION (CRITICAL) ---
    user_id = request.args.get("id")
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE id = '%s'" % user_id
    cursor.execute(query)

    # --- 3. INSECURE DESERIALIZATION (CRITICAL) ---
    data = request.args.get("data")
    if data:
        decoded_data = base64.b64decode(data)
        pickle.loads(decoded_data) 

    # --- 4. COMMAND INJECTION (HIGH) ---
    filename = request.args.get("filename")
    os.system("ls -l " + filename)

    # --- 5. PATH TRAVERSAL (HIGH) ---
    with open(os.path.join("uploads", filename), "r") as f:
        content = f.read()

    # --- 6. RESOURCE LEAK (NEW: WARNING) ---
    # Opening a file without a 'with' block or .close() call
    # CodeQL: py/resource-leak
    log_file = open("access_log.txt", "a")
    log_file.write(f"Access from {user_id}\n")
    # intentionally not closed

    # --- 7. DEPRECATED FUNCTION (NEW: NOTE/WARNING) ---
    # base64.encodestring is deprecated in Python 3.x
    # CodeQL: py/deprecated-method-call
    sample_text = b"test"
    encoded_sample = base64.encodestring(sample_text)

    # --- 8. CROSS-SITE SCRIPTING - XSS (MEDIUM) ---
    name = request.args.get("name", "Guest")
    template = "<h1>Welcome %s</h1>" % name
    
    # --- 9. BROKEN CRYPTOGRAPHY & WEAK HASH (MEDIUM) ---
    password = request.args.get("password")
    hashed_pw = hashlib.md5(password.encode()).hexdigest()
    
    # --- 10. LEGACY/DEPRECATED CRYPTO (NEW: WARNING) ---
    # The 'crypt' module is deprecated since Python 3.11
    # CodeQL: py/weak-cryptographic-hash
    legacy_hash = crypt.crypt(password, "salt")

    # --- 11. INSECURE COMPARISON (NEW: WARNING) ---
    # Using '==' for secret comparison instead of hmac.compare_digest
    # CodeQL: py/timing-attack
    provided_token = request.args.get("token")
    SECRET_TOKEN = "admin_secret_123"
    if provided_token == SECRET_TOKEN:
        print("Authenticated")

    # --- 12. INSECURE COOKIE SETTINGS (LOW/INFO) ---
    response = make_response(render_template_string(template))
    response.set_cookie("session_id", "12345", httponly=False, secure=False)

    # --- 13. CLEAR-TEXT LOGGING (LOW) ---
    print(f"User {user_id} logged in with password {password}")

    return response

@app.route("/error")
def error_leak():
    # --- 14. BROAD EXCEPTION & INFO EXPOSURE (LOW) ---
    try:
        1 / 0
    except: # NEW: Catching all exceptions (py/broad-exception)
        import traceback
        # py/full-precision-money-leak or py/stack-trace-exposure
        return traceback.format_exc(), 500

@app.route("/redirect")
def open_redirect():
    # --- 15. OPEN REDIRECT (NEW: HIGH) ---
    # CodeQL: py/open-redirect
    target = request.args.get("url")
    return make_response("", 302, {"Location": target})

if __name__ == "__main__":
    # --- 16. DEBUG MODE ENABLED ---
    app.run(debug=True, host="0.0.0.0")
