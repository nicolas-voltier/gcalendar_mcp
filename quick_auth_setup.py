"""
Quick Google Calendar OAuth setup script
Reads from credentials.json and generates token.json
"""
import json
import requests
import webbrowser
import urllib.parse
from pathlib import Path

def quick_google_auth():
    # Paths - use current working directory
    creds_path = Path.cwd() / 'credentials.json'
    token_path = Path.cwd() / 'token.json'
    
    # Load credentials
    if not creds_path.exists():
        print(f"❌ Credentials file not found: {creds_path}")
        print("Download credentials.json from Google Cloud Console first!")
        return
    
    with open(creds_path, 'r') as f:
        creds = json.load(f)
    
    # Extract client info (works for both 'installed' and 'web' app types)
    if 'installed' in creds:
        client_info = creds['installed']
    elif 'web' in creds:
        client_info = creds['web']
    else:
        print("❌ Invalid credentials.json format")
        return
    
    client_id = client_info['client_id']
    client_secret = client_info['client_secret']
    
    # Build auth URL
    params = {
        'client_id': client_id,
        'redirect_uri': 'http://localhost:8080',
        'scope': 'https://www.googleapis.com/auth/calendar',
        'response_type': 'code',
        'access_type': 'offline',
        'prompt': 'consent'
    }
    
    auth_url = f"https://accounts.google.com/o/oauth2/auth?{urllib.parse.urlencode(params)}"
    
    print("🔗 Opening Google authorization page...")
    webbrowser.open(auth_url)
    print("\n📋 After authorizing, copy the 'code' parameter from the URL")
    print("The URL will look like: http://localhost:8080/?code=4/0AanwX...")
    print("Copy everything after 'code=' (before any '&' if present)")
    
    # Get code from user
    code = input("Paste authorization code: ").strip()
    
    # Exchange for tokens
    token_data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': 'http://localhost:8080'
    }
    
    print("🔄 Getting tokens...")
    response = requests.post('https://oauth2.googleapis.com/token', data=token_data)
    
    if response.status_code == 200:
        tokens = response.json()
        
        # Add client credentials to the token file (MCP server expects them)
        tokens['client_id'] = client_id
        tokens['client_secret'] = client_secret
        
        # Save tokens with credentials
        token_path.parent.mkdir(parents=True, exist_ok=True)
        with open(token_path, 'w') as f:
            json.dump(tokens, f, indent=2)
        
        print(f"✅ Success! Token saved to: {token_path}")
        print("🚀 Your MCP server should now work!")
        
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    quick_google_auth()
