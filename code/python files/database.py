import pickle
from bson.binary import Binary
from pymongo import MongoClient
import os
import face_recognition as fr
import hashlib

# Initialize MongoDB client
client = MongoClient('localhost', 27017)
db = client['face_recognition']

def insert_face(name, encoding, image_hash):
    # Convert encoding to binary for storage
    encoding_binary = Binary(pickle.dumps(encoding, protocol=2), subtype=128)
    # Insert into the collection named after the person
    face_collection = db[name]
    face_collection.insert_one({"encoding": encoding_binary})

def update_encoded_faces(face_repository_path):
    faces = {}
    for root, dirs, files in os.walk(face_repository_path):
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg", ".png")):
                name = os.path.basename(root)
                image_path = os.path.join(root, file)
                image_hash = get_image_hash(image_path)
                if not is_face_existing(name, image_hash):
                    encoding = unknown_image_encoded(image_path)
                    if encoding is not None:
                        insert_face(name, encoding, image_hash)
                        faces[name] = encoding
    return faces

def load_encoded_faces():
    faces = {}
    for collection_name in db.list_collection_names():
        if collection_name != 'images':
            face_collection = db[collection_name]
            for face_data in face_collection.find():
                encoding = pickle.loads(face_data["encoding"])
                faces[collection_name] = encoding
    return faces

def unknown_image_encoded(img_path):
    face = fr.load_image_file(img_path)
    encodings = fr.face_encodings(face)
    if encodings:
        return encodings[0]
    else:
        return None

def get_image_hash(image_path):
    with open(image_path, "rb") as f:
        bytes = f.read()
        return hashlib.md5(bytes).hexdigest()

def is_face_existing(name, image_hash):
    face_collection = db[name]
    return face_collection.find_one({'hash': image_hash}) is not None

def insert_face_image(name, encoding, image_path):
    image_hash = get_image_hash(image_path)
    if not is_face_existing(name, image_hash):
        insert_face(name, encoding, image_hash)
