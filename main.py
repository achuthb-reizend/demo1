import os
import sqlite3
import pickle
import base64
import hashlib
import math  # CodeQL NOTE: unused import

# --- 1. TRIGGER: DEPRECATED MODULES ---
import imp   # Deprecated module
import cgi   # Deprecated module

from flask import Flask, request, make_response, render_template_string

app = Flask(__name__)

@app.route("/vulnerable-complex")
def vulnerable_complex():
    # TODO: Refactor this function to improve security
    # FIXME: Remove deprecated APIs and unsafe patterns

    unused_variable = "this variable is never used"  # CodeQL NOTE: unused variable

    user_id = request.args.get("id")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # NOTE: This query is intentionally unsafe for testing static analysis
    query = "SELECT * FROM users WHERE id = '%s'" % user_id
    cursor.execute(query)

    # --- Deprecated API usage ---
    try:
        imp.find_module('os')  # Deprecated call
    except Exception:  # CodeQL WARNING: broad exception catch
        pass

    # Deprecated function
    text_to_escape = request.args.get("text", "")
    escaped_text = cgi.escape(text_to_escape)

    # Deprecated base64 API
    legacy_b64 = base64.encodestring(b"test")

    # Weak cryptographic hash (non-critical severity)
    weak_hash = hashlib.md5(b"password").hexdigest()  # CodeQL WARNING

    # Commented-out code (CodeQL NOTE)
    # pickle.loads(base64.b64decode("dGVzdA=="))

    data = request.args.get("data")
    if data:
        pickle.loads(base64.b64decode(data))

    name = request.args.get("name", "Guest")
    template = "<h1>Welcome %s</h1>" % name

    response = make_response(render_template_string(template))
    return response

if __name__ == "__main__":
    app.run(debug=True)
