from google.cloud import firestore
from dotenv import load_dotenv
load_dotenv()
# Initialize Firestore client
db = firestore.Client()

visitor_ref = db.collection('visitors')