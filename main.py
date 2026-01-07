import os
import sqlite3
import pickle
import base64
import hashlib
import sys # NOTE: Unused import (py/unused-import)
import math # NOTE: Unused import (py/unused-import)
from flask import Flask, request, make_response, render_template_string

# --- 1. WARNING: DUPLICATE IMPORT ---
# CodeQL ID: py/module-imported-multiple-times
import os 

app = Flask(__name__)

# --- 2. NOTE: UNUSED GLOBAL VARIABLE ---
# CodeQL ID: py/unused-global-variable
UNUSED_CONFIG_KEY = "SECRET_12345"

@app.route("/vulnerable-complex")
def vulnerable_complex():
    # --- [CRITICAL ERRORS REMAIN] ---
    user_id = request.args.get("id")
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE id = '%s'" % user_id
    cursor.execute(query)

    data = request.args.get("data")
    if data:
        pickle.loads(base64.b64decode(data)) 

    # --- 3. WARNING: DEPRECATED FUNCTION ---
    # CodeQL ID: py/deprecated-method-call
    # base64.encodestring was deprecated in Python 3.1
    legacy_encoded = base64.encodestring(b"test_data")

    # --- 4. WARNING: UNREACHABLE CODE ---
    # CodeQL ID: py/unreachable-statement
    return_val = "Done"
    return return_val
    print("This line will never be reached") # Dead code

    # --- 5. WARNING: REDUNDANT ASSIGNMENT ---
    # CodeQL ID: py/redundant-assignment
    temp_count = 10
    temp_count = temp_count # Self-assignment

    # --- 6. NOTE: UNUSED LOCAL VARIABLE ---
    # CodeQL ID: py/unused-local-variable
    internal_flag = "DEBUG_OFF" # Defined but never read

    # --- 7. WARNING: COMPARISON OF IDENTICAL VALUES ---
    # CodeQL ID: py/comparison-of-identical-values
    if user_id == user_id:
        pass

    return "Check your Security tab for quality alerts!"

# --- 8. WARNING: EMPTY EXCEPT BLOCK ---
# CodeQL ID: py/empty-except
try:
    x = 1 / 0
except:
    pass # This suppresses all errors and is a major quality warning

if __name__ == "__main__":
    app.run(debug=True)
