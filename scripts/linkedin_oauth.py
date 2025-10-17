#!/usr/bin/env python3
"""
LinkedIn OAuth 2.0 Helper Script
Automates the OAuth flow to get access token and user ID
"""
import os
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv, set_key
import requests

# Configuration
REDIRECT_URI = "http://localhost:8000/callback"
SCOPES = "openid profile w_member_social"

# Global variable to capture authorization code
auth_code = None


class OAuthHandler(BaseHTTPRequestHandler):
    """HTTP handler to capture OAuth callback"""
    
    def do_GET(self):
        global auth_code
        
        # Parse the callback URL
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        
        if 'code' in params:
            auth_code = params['code'][0]
            
            # Send success response
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = """
            <html>
            <head><title>LinkedIn OAuth Success</title></head>
            <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
                <h1 style="color: #0077B5;">✅ Authorization Successful!</h1>
                <p style="font-size: 18px;">You can close this window and return to the terminal.</p>
                <p style="color: #666;">The automation will continue in the command prompt...</p>
                <script>setTimeout(function(){ window.close(); }, 3000);</script>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = """
            <html>
            <head><title>LinkedIn OAuth Error</title></head>
            <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
                <h1 style="color: #D32F2F;">❌ Authorization Failed</h1>
                <p>Please check the terminal for details.</p>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
    
    def log_message(self, format, *args):
        """Suppress log messages"""
        pass


def get_authorization_code(client_id):
    """Step 1: Get authorization code"""
    auth_url = (
        f"https://www.linkedin.com/oauth/v2/authorization"
        f"?response_type=code"
        f"&client_id={client_id}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope={SCOPES.replace(' ', '%20')}"
    )
    
    print("\n" + "="*60)
    print("🔐 LinkedIn OAuth 2.0 - Step 1: Authorization")
    print("="*60)
    print(f"\nOpening browser for authorization...")
    print(f"\n📝 Authorization URL:")
    print(f"   {auth_url}\n")
    
    # Open browser
    print("⏳ Opening your default browser...")
    webbrowser.open(auth_url)
    
    # Start local server to capture callback
    print("\n⏳ Waiting for authorization...")
    print("   1. A browser window should open")
    print("   2. Sign in to LinkedIn if needed")
    print("   3. Click 'Allow' to authorize the app")
    print("   4. The browser will redirect back automatically\n")
    
    try:
        server = HTTPServer(('localhost', 8000), OAuthHandler)
        server.handle_request()  # Handle one request then stop
    except OSError as e:
        print(f"\n❌ Error: Port 8000 is already in use")
        print("   Please close any applications using port 8000 and try again")
        print(f"   Error details: {str(e)}")
        return None
    
    return auth_code


def exchange_code_for_token(client_id, client_secret, auth_code):
    """Step 2: Exchange authorization code for access token"""
    print("\n" + "="*60)
    print("🔄 Step 2: Exchanging code for access token")
    print("="*60)
    
    token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    
    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': REDIRECT_URI,
        'client_id': client_id,
        'client_secret': client_secret
    }
    
    try:
        response = requests.post(token_url, data=data)
        
        if response.status_code == 200:
            token_data = response.json()
            expires_days = token_data['expires_in'] // 86400
            print(f"✅ Access token obtained successfully!")
            print(f"   Token type: {token_data.get('token_type', 'Bearer')}")
            print(f"   Expires in: {token_data['expires_in']} seconds (~{expires_days} days)")
            print(f"   Scopes: {token_data.get('scope', 'N/A')}")
            return token_data['access_token']
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception occurred: {str(e)}")
        return None


def get_user_profile(access_token):
    """Step 3: Get LinkedIn user ID"""
    print("\n" + "="*60)
    print("👤 Step 3: Fetching user profile")
    print("="*60)
    
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    try:
        response = requests.get('https://api.linkedin.com/v2/me', headers=headers)
        
        if response.status_code == 200:
            profile = response.json()
            user_id = profile['id']
            first_name = profile.get('localizedFirstName', 'N/A')
            last_name = profile.get('localizedLastName', 'N/A')
            print(f"✅ Profile retrieved successfully!")
            print(f"   Name: {first_name} {last_name}")
            print(f"   User ID: {user_id}")
            return user_id
        else:
            print(f"❌ Error fetching profile: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception occurred: {str(e)}")
        return None


def save_to_env(access_token, user_id):
    """Step 4: Save credentials to .env file"""
    print("\n" + "="*60)
    print("💾 Step 4: Saving to .env file")
    print("="*60)
    
    env_file = '.env'
    
    if not os.path.exists(env_file):
        print(f"Creating {env_file}...")
        with open(env_file, 'w') as f:
            f.write("")
    
    try:
        set_key(env_file, 'LINKEDIN_ACCESS_TOKEN', access_token)
        set_key(env_file, 'LINKEDIN_USER_ID', user_id)
        
        print(f"✅ Credentials saved to {env_file}")
        print(f"\n   LINKEDIN_ACCESS_TOKEN: {access_token[:20]}... [SAVED]")
        print(f"   LINKEDIN_USER_ID: {user_id} [SAVED]")
        return True
    except Exception as e:
        print(f"❌ Error saving to .env: {str(e)}")
        return False


def main():
    """Main OAuth flow"""
    print("\n" + "="*60)
    print("🚀 LinkedIn OAuth 2.0 Setup Wizard")
    print("="*60)
    print("\nThis script will help you get LinkedIn API credentials")
    print("in 4 easy steps.\n")
    
    # Load existing .env
    load_dotenv()
    
    # Get credentials
    client_id = os.getenv('LINKEDIN_CLIENT_ID')
    client_secret = os.getenv('LINKEDIN_CLIENT_SECRET')
    
    if not client_id or client_id == 'your_linkedin_client_id_here':
        print("\n❌ Error: LINKEDIN_CLIENT_ID not found or not set in .env")
        print("\n📋 Please complete these steps first:")
        print("   1. Go to: https://www.linkedin.com/developers/apps")
        print("   2. Click on your app (or create one)")
        print("   3. Go to 'Auth' tab")
        print("   4. Copy Client ID and Client Secret")
        print("   5. Add them to your .env file:")
        print("      LINKEDIN_CLIENT_ID=your_client_id")
        print("      LINKEDIN_CLIENT_SECRET=your_client_secret")
        print("\n   Then run this script again.")
        return
    
    if not client_secret or client_secret == 'your_linkedin_client_secret_here':
        print("\n❌ Error: LINKEDIN_CLIENT_SECRET not found or not set in .env")
        print("\n📋 Please add your Client Secret to .env file:")
        print("   LINKEDIN_CLIENT_SECRET=your_client_secret")
        print("\n   Then run this script again.")
        return
    
    print(f"\n✅ Found Client ID: {client_id[:15]}...")
    print(f"✅ Found Client Secret: {client_secret[:15]}...")
    
    # Step 1: Get authorization code
    auth_code = get_authorization_code(client_id)
    
    if not auth_code:
        print("\n❌ Failed to get authorization code")
        print("   Please try again or check the troubleshooting guide")
        return
    
    print(f"✅ Authorization code received: {auth_code[:25]}...")
    
    # Step 2: Exchange for access token
    access_token = exchange_code_for_token(client_id, client_secret, auth_code)
    
    if not access_token:
        print("\n❌ Failed to get access token")
        print("   Please check your Client ID and Client Secret")
        return
    
    # Step 3: Get user profile
    user_id = get_user_profile(access_token)
    
    if not user_id:
        print("\n❌ Failed to get user ID")
        print("   But access token was obtained successfully")
        print("   You can still add the token to .env manually")
        return
    
    # Step 4: Save to .env
    if not save_to_env(access_token, user_id):
        print("\n⚠️  Failed to save to .env automatically")
        print(f"\n📝 Please add these manually to your .env file:")
        print(f"   LINKEDIN_ACCESS_TOKEN={access_token}")
        print(f"   LINKEDIN_USER_ID={user_id}")
        return
    
    print("\n" + "="*60)
    print("🎉 LinkedIn OAuth Setup Complete!")
    print("="*60)
    print("\n✅ Your LinkedIn credentials are now saved in .env")
    print("✅ You can now use the automation system to post to LinkedIn!")
    print("\n📝 Next steps:")
    print("   1. Test without posting:")
    print("      python main.py --mode manual --dry-run")
    print("\n   2. Test with actual posting:")
    print("      python main.py --mode manual")
    print("\n   3. Start automation:")
    print("      python main.py --mode auto")
    print("\n💡 Tip: Your access token is valid for ~60 days")
    print("   Run this script again when it expires")
    print("\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user")
        print("   You can run the script again anytime")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        print("   Please check the troubleshooting guide or try again")
