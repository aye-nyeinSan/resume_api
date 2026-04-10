from google.cloud import firestore

# Initialize Firestore client
db = firestore.Client()

visitor_ref = db.collection('visitors')