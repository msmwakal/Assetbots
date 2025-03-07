# Assetbots Email Sender API key: 6C806C3558BCBCD28E584E4877182A8A

import os
import base64
import requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.text import MIMEText

# Assetbots API URL and Key
ASSETBOTS_API_URL = "https://api.assetbots.com/v1/checkouts"
ASSETBOTS_API_KEY = "76C806C3558BCBCD28E584E4877182A8A"

# Gmail API Scopes
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

# Authenticate with Gmail API
def authenticate_gmail():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

# Send Email
def send_email(recipient, asset_name):
    creds = authenticate_gmail()
    service = build("gmail", "v1", credentials=creds)

    message = MIMEText(f"The asset '{asset_name}' has been checked out.")
    message["to"] = recipient
    message["subject"] = "Asset Checkout Notification"
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    service.users().messages().send(userId="me", body={"raw": raw_message}).execute()
    print(f"Email sent to {recipient}")

# Monitor Asset Checkouts
def monitor_checkouts():
    headers = {"Authorization": f"Bearer {ASSETBOTS_API_KEY}"}
    response = requests.get(ASSETBOTS_API_URL, headers=headers)
    if response.status_code == 200:
        checkouts = response.json()
        for checkout in checkouts:
            user_email = checkout.get("user", {}).get("email")
            asset_name = checkout.get("asset", {}).get("name")
            #if user_email and asset_name:
                #send_email(user_email, asset_name)
    else:
        print(f"Failed to retrieve checkouts: {response.status_code}")

if __name__ == "__main__":
    monitor_checkouts()

