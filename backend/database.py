import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate(r"C:\Users\Faleel Mohsin\Documents\claude\backend\serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
users_collection = db.collection("users")