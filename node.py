import boto3

# This triggers CodeQL's "Hardcoded credentials" (CWE-798)
def login():
    access_key = "AKIAEXAMPLE123456789"
    secret_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    
    # Passing them into a constructor or function makes CodeQL flag it
    client = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    return client
