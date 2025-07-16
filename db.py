# db.py
from pymongo import MongoClient

def connect_db():
    # Conexión local
    client = MongoClient("")
    db = client["indexMovies"]
    return db