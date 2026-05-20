import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Scopes required for Google Calendar and Gmail and Drive
SCOPES = [
    'https://www.googleapis.com/auth/calendar.events',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/drive'
]

def generate_token():
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET")

    if not client_id or not client_secret:
        print("Error: GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET not found in .env file.")
        return

    # Construct client config dictionary
    client_config = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost:8080/"]
        }
    }

    try:
        # If client credentials are mock/placeholders, generate a mock token.json directly
        if "mock" in client_id.lower() or "mock" in client_secret.lower():
            mock_creds = {
                "token": "mock_access_token_value",
                "refresh_token": "mock_refresh_token_value",
                "token_uri": "https://oauth2.googleapis.com/token",
                "client_id": client_id,
                "client_secret": client_secret,
                "scopes": SCOPES,
                "expiry": "2030-01-01T00:00:00Z"
            }
            with open('token.json', 'w') as token_file:
                json.dump(mock_creds, token_file, indent=2)
            print("\nSuccess! [MOCK] token.json has been generated for development/testing.")
            return

        # Run the OAuth2 flow
        flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
        creds = flow.run_local_server(port=8080)

        # Save the credentials to token.json
        with open('token.json', 'w') as token_file:
            token_file.write(creds.to_json())
        
        print("\nSuccess! token.json has been generated.")
        print("The application will now be able to create real Google Meet links.")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    generate_token()

