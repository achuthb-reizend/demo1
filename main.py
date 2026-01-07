import os
import sqlite3
import pickle
import base64
import hashlib
# --- 1. TRIGGER: DEPRECATED MODULES ---
import imp  # Trigger for: 'imp' module is deprecated
import cgi  # Trigger for: 'cgi' module is deprecated
from flask import Flask, request, make_response, render_template_string

app = Flask(__name__)

@app.route("/vulnerable-complex")
def vulnerable_complex():
    # --- [CRITICAL ERRORS] ---
    user_id = request.args.get("id")
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE id = '%s'" % user_id
    cursor.execute(query)

    # --- 2. TRIGGER: DEPRECATED FUNCTION CALLS ---
    # CodeQL ID: py/deprecated-method-call (CWE-477)
    # imp.find_module is a classic deprecated call
    try:
        imp.find_module('os') 
    except:
        pass

    # cgi.escape was removed/deprecated in favor of html.escape
    text_to_escape = request.args.get("text", "")
    escaped_text = cgi.escape(text_to_escape) 

    # base64.encodestring (Another attempt)
    legacy_b64 = base64.encodestring(b"test")

    # --- [OTHER ORIGINAL ERRORS] ---
    data = request.args.get("data")
    if data:
        pickle.loads(base64.b64decode(data)) 

    name = request.args.get("name", "Guest")
    template = "<h1>Welcome %s</h1>" % name
    response = make_response(render_template_string(template))
    return response

if __name__ == "__main__":
    app.run(debug=True)
