import os
import sqlite3
from flask import Flask, request

app = Flask(__name__)

# 1. SECRET SCANNING TRIGGER
# Hardcoding an AWS Access Key (even a fake one follows a detectable pattern)
AWS_ACCESS_KEY = "AKIAIMNO7YBX3TOEXAMPLE" 
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

@app.route("/user-info")
def get_user():
    # 2. CODEQL TRIGGER (SQL Injection)
    # This is a "Tainted Input" vulnerability where user input flows directly into a query.
    user_id = request.args.get("id")
    
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    # Dangerous: string formatting allows SQL Injection
    query = "SELECT * FROM users WHERE id = '%s'" % user_id
    cursor.execute(query) 
    
    return str(cursor.fetchone())

if __name__ == "__main__":
    app.run(debug=True)
