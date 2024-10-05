Description This project implements a face recognition system using Flask, OpenCV, and Face Recognition libraries. It provides APIs to train, identify, and delete faces from the recognition system.

Features Train the system with multiple face images. Identify faces in images. Manage the face database (add/delete). API documentation with Swagger.

Installation Prerequisites Python 3.7 or higher MongoDB

Dependencies To install the required dependencies, run: pip install -r requirements.txt

Steps for Setting Up the Project:

Download and install Python.

Set Up a Virtual Environment in following steps a) Create a virtual environment: python -m venv venv b) Activate the virtual environment: venv\Scripts\activate

Install Required Packages i.e. flask, flask-cors, face_recognition, opencv-python numpy, flasgger, pymongo

Create Project Structure in the specified method

project/ ├── app.py ├── swagger/ │ ├── train.yml │ ├── identify.yml │ └── delete.yml ├── database.py ├── venv/ └── requirements.txt

Create database.py.
Create Swagger YML Files.
Configure VS Code for Flask.
Run the Flask Application: flask run
