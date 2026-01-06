import os
import sqlite3
from flask import Flask, request

app = Flask(__name__)

# 1. SECRET SCANNING TRIGGER
# Hardcoding an AWS Access Key (even a fake one follows a detectable pattern)
# Use a random string of 20 chars for the ID and 40 for the Secret
AWS_ACCESS_KEY = "AKIA5F7D3X9R2EXAMPLE" 
AWS_SECRET_KEY = "u9+G8kLp2mN5qR8vWzX1yB4c7d0e3f6g9h2j5k8l"
STRIPE_KEY = "sk_live_51MzXkL2eY6ghSjR8nK9pL2mN5qR8vWzX";
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
