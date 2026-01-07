"""
Quick Google Calendar OAuth setup script
Reads from credentials.json and generates token.json
Uses the same OAuth flow as calendar_mcp_server.py
"""
import json
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow

# OAuth scopes
SCOPES = ['https://www.googleapis.com/auth/calendar']

def quick_google_auth():
    # Paths - use current working directory
    creds_path = Path.cwd() / 'credentials.json'
    token_path = Path.cwd() / 'token.json'
    
    print("Google Calendar OAuth Setup")
    print("=" * 50)
    
    # Check for credentials file
    if not creds_path.exists():
        print(f"\n❌ Credentials file not found: {creds_path}")
        print("\nPlease download your OAuth credentials from Google Cloud Console:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Create/select a project")
        print("3. Enable Google Calendar API")
        print("4. Create OAuth credentials (Desktop client OAuth ID)")
        print(f"5. Download and save as '{creds_path.name}' in this directory")
        return False
    
    print(f"\n✅ Found credentials file: {creds_path}")
    
    # Check if token already exists
    if token_path.exists():
        print(f"\n⚠️  Existing token file found: {token_path}")
        response = input("Delete existing token to force re-authentication? (y/n): ").strip().lower()
        if response == 'y':
            token_path.unlink()
            print(f"✅ Deleted {token_path}")
        else:
            print("Keeping existing token file.")
            return True
    
    print("\n🔗 Starting OAuth flow...")
    print("A browser window will open for Google authentication.")
    print("Please authorize the application to access your Google Calendar.\n")
    
    try:
        # Use the same OAuth flow as calendar_mcp_server.py
        flow = InstalledAppFlow.from_client_secrets_file(
            str(creds_path), SCOPES)
        creds = flow.run_local_server(port=0)
        
        print("\n✅ OAuth flow completed successfully!")
        
        # Save credentials in the format expected by calendar_mcp_server.py
        token_content = {
            'token': creds.token,
            'refresh_token': creds.refresh_token,
            'token_uri': creds.token_uri,
            'client_id': creds.client_id,
            'client_secret': creds.client_secret,
            'scopes': creds.scopes
        }
        
        token_path.write_text(json.dumps(token_content, indent=2))
        print(f"✅ Token saved to: {token_path}")
        print("\n🚀 Your MCP server should now work!")
        print("=" * 50)
        return True
        
    except Exception as e:
        print(f"\n❌ Error during OAuth flow: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure your OAuth client is created as 'Desktop app' (not 'Web application')")
        print("2. Check that Google Calendar API is enabled in your project")
        print("3. Verify your credentials.json file is correct")
        print("=" * 50)
        return False

if __name__ == "__main__":
    quick_google_auth()
