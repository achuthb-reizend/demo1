import os
import sqlite3
import pickle
import base64
import hashlib
import crypt
import hmac
import sys # Trigger for Recommendation: Unused import (if not used below)
import math # Trigger for Recommendation: Unused import
from flask import Flask, request, make_response, render_template_string

# --- 1. CODE QUALITY: DUPLICATE IMPORT (WARNING) ---
# CodeQL: py/module-imported-multiple-times
import os 

app = Flask(__name__)

# --- 2. CODE QUALITY: REDUNDANT ASSIGNMENT (WARNING) ---
# CodeQL: py/redundant-assignment
def redundant_stuff():
    x = 10
    x = x # Self-assignment

@app.route("/vulnerable-complex")
def vulnerable_complex():
    # --- [KEEPING PREVIOUS CRITICAL ERRORS] ---
    user_id = request.args.get("id")
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE id = '%s'" % user_id
    cursor.execute(query)

    data = request.args.get("data")
    if data:
        decoded_data = base64.b64decode(data)
        pickle.loads(decoded_data) 

    filename = request.args.get("filename")
    os.system("ls -l " + filename)

    # --- 3. CODE QUALITY: UNREACHABLE CODE (WARNING) ---
    # CodeQL: py/unreachable-statement
    return_val = "Process complete"
    return return_val
    print("This will never execute!") # Logic error

    # --- 4. CODE QUALITY: REDUNDANT COMPARISON (WARNING) ---
    # CodeQL: py/redundant-comparison or py/comparison-of-identical-values
    val = 10
    if val == 10 and val == 10:
        pass

    # --- 5. CODE QUALITY: MULTIPLE DEFINITION (WARNING) ---
    # CodeQL: py/multiple-definition
    temp_var = "initial"
    temp_var = "overwrite" # Overwriting without using the first one
    print(temp_var)

    # --- 6. CODE QUALITY: IMPLICIT STRING CONCAT IN LIST (NOTE/WARNING) ---
    # CodeQL: py/implicit-string-concatenation-in-list
    # Missing comma between strings in a list
    my_list = [
        "first_item"
        "second_item" # This becomes "first_itemsecond_item"
    ]

    # --- 7. DEPRECATED FUNCTION (NOTE/WARNING) ---
    # base64.encodestring is deprecated in Python 3
    # CodeQL: py/deprecated-method-call
    sample_text = b"test"
    encoded_sample = base64.encodestring(sample_text)

    # --- [REMAINING ORIGINAL CODE] ---
    name = request.args.get("name", "Guest")
    template = "<h1>Welcome %s</h1>" % name
    password = request.args.get("password")
    hashed_pw = hashlib.md5(password.encode()).hexdigest()
    
    response = make_response(render_template_string(template))
    response.set_cookie("session_id", "12345", httponly=False, secure=False)
    return response

@app.route("/error")
def error_leak():
    # --- 8. CODE QUALITY: BROAD EXCEPTION (WARNING) ---
    # CodeQL: py/broad-exception
    try:
        1 / 0
    except: # Catch-all is poor practice
        return "Error", 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
