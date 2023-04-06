from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


# Additions for integrating Google doc with app.
# See documentation here: https://developers.google.com/docs/api/quickstart/python
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy()

# Set up API access to a test document.

DOCUMENT_ID = '1VkvEXv8xn6kL020lkKkh4saBXiQYkxBgPNdGWnN6b_w' # Document ID copied from the URL of the document.
credentials = Credentials.from_authorized_user_file('credentials.json') # Super secure credentials file. Fix later. Keybase or similar?
SCOPES = ['https://www.googleapis.com/auth/documents'] # Source: https://developers.google.com/identity/protocols/oauth2/scopes#docs

# Get a document object from the API. 
try:
    service = build('docs', 'v1', credentials=credentials)
    document = service.documents().get(documentId=DOCUMENT_ID).execute()
except HttpError as e:
    print(e)
    

migrate = Migrate(app, db)
db.init_app(app)