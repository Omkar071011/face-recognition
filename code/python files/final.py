import cv2
import numpy as np
import face_recognition as fr
from flask import Flask, request, jsonify
from flask_cors import CORS
import time
from database import insert_face, db, load_encoded_faces
from flasgger import Swagger, swag_from
app = Flask(__name__)
CORS(app)
swagger = Swagger(app)
# Global variable to store encoded faces
faces = {}

# Set the threshold value
FACE_RECOGNITION_THRESHOLD = 0.49

def reload_faces():
    global faces
    faces = load_encoded_faces()

# Initial load of encoded faces
reload_faces()

@app.route('/train', methods=['POST'])
@swag_from('swagger/train.yml')
def train():
    if len(request.files) != 5:
        return jsonify({"error": "Exactly 5 images are required"}), 400

    label = request.form.get('label')
    if not label:
        return jsonify({"error": "Label is required"}), 400

    start_time = time.time()
    new_faces = {}

    for i in range(1, 6):
        file = request.files.get(f'image{i}')
        if file:
            img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
            if img is not None:
                face_locations = fr.face_locations(img)
                face_encodings = fr.face_encodings(img, face_locations)
                if face_encodings:
                    if label not in new_faces:
                        new_faces[label] = []
                    new_faces[label].append((face_encodings[0], file.read()))
                    # Store the uploaded image in the database for training
                    insert_face(label, face_encodings[0], file.read())

    # Reload faces after training
    reload_faces()
    update_encoded_faces_time = time.time() - start_time

    return jsonify({"message": "Training complete", "faces": list(new_faces.keys()), "update_encoded_faces_time": update_encoded_faces_time})


@app.route('/identify', methods=['POST'])
@swag_from('swagger/identify.yml')
def identify():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files['image']
    start_time = time.time()
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    image_decode_time = time.time() - start_time

    if img is None:
        return jsonify({"error": "Invalid image"}), 400

    # Resize image for faster processing
    small_img = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)

    start_time = time.time()
    face_locations = fr.face_locations(small_img)
    # Scale back up face locations to the original image size
    face_locations = [(int(top*4), int(right*4), int(bottom*4), int(left*4)) for top, right, bottom, left in face_locations]
    face_locations_time = time.time() - start_time

    if not face_locations:
        return jsonify({"error": "No faces found"}), 400

    # Find the face with the maximum bounding box area
    max_area = 0
    max_face_location = None
    for (top, right, bottom, left) in face_locations:
        area = (right - left) * (bottom - top)
        if area > max_area:
            max_area = area
            max_face_location = (top, right, bottom, left)

    start_time = time.time()
    unknown_face_encodings = fr.face_encodings(img, [max_face_location])
    face_encodings_time = time.time() - start_time

    face_names = []
    if unknown_face_encodings:
        face_encoding = unknown_face_encodings[0]
        start_time = time.time()
        name = "Unknown"
        face_distances = fr.face_distance(list(faces.values()), face_encoding)
        face_distance_time = time.time() - start_time

        if len(face_distances) > 0:
            best_match_index = np.argmin(face_distances)
            matches = fr.compare_faces(list(faces.values()), face_encoding)
            # Debug statement to check face distances and threshold comparison
            print(f"Face distances: {face_distances}, Best match index: {best_match_index}, Best match distance: {face_distances[best_match_index]}, Threshold: {FACE_RECOGNITION_THRESHOLD}")
            if matches[best_match_index] and face_distances[best_match_index] < FACE_RECOGNITION_THRESHOLD:
                name = list(faces.keys())[best_match_index]
        face_names.append(name)

 


    return jsonify({"faces": face_names})
@app.route('/delete', methods=['DELETE'])
@swag_from('swagger/delete.yml')
def delete():
    data = request.get_json()
    label = data.get('label')
    if not label:
        return jsonify({"error": "No label provided"}), 400

    # Check if the collection (label) exists in the database
    if label not in db.list_collection_names():
        return jsonify({"error": f"Label '{label}' does not exist in the database"}), 404

    # Delete the faces from the collection
    db.drop_collection(label)

    # Reload faces after deletion
    reload_faces()

    return jsonify({"message": f"Deleted label '{label}'"}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
