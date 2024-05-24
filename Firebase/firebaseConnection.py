import firebase_admin
from datetime import datetime

import pandas as pd
from firebase_admin import credentials, db, firestore


def registering_user(username, password):
    db = firestore.client()
    user_cred = {
        'username': username,
        'password': password
    }

    doc_ref = db.collection("users").document(username)

    doc_ref.set(user_cred)

def login_user(username, password):
    username_matched = False
    password_matched = False

    db = firestore.client()
    collection_ref = db.collection("users")
    documents = collection_ref.list_documents()
    document_list = [doc.id for doc in documents]

    if username in document_list:
        doc_ref = db.collection("users").document(username)
        ret_password = doc_ref.get().to_dict().get("password")
        username_matched = True
        if ret_password == password:
            password_matched = True

    return username_matched, password_matched
