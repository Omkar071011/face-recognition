# 🧠 Face Recognition System API

This project implements a **Face Recognition System** using **Flask**, **OpenCV**, and the **face_recognition** library. It provides REST APIs to **train**, **identify**, and **delete** faces, along with Swagger-based documentation.

---

## 🚀 Features

- ✅ Train the system with multiple face images  
- ✅ Identify faces in uploaded images  
- ✅ Add or delete faces from the database  
- ✅ API documentation via Swagger (`.yml` files)

---

## 🛠️ Installation

### ✅ Prerequisites

- Python 3.7 or higher  
- MongoDB installed and running locally or on a server

---

## 📁 Project Structure

project/
├── app.py
├── database.py
├── swagger/
│ ├── train.yml
│ ├── identify.yml
│ └── delete.yml
├── requirements.txt
└── venv/


---

## ⚙️ Setup Instructions

### 1️⃣ Install Python (if not already)

[Download Python](https://www.python.org/downloads/)

---

### 2️⃣ Create and Activate Virtual Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

### 3️⃣ Install Required Packages

#### Option 1: Install from `requirements.txt`

```bash
pip install flask flask-cors face_recognition opencv-python numpy flasgger pymongo

### 4 Create `database.py`

This file handles all interactions with the MongoDB database.

You should define functions to:

- Add face data to the database
- Retrieve face data for identification
- Delete face data from the database

Example (basic structure):

```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["face_db"]
collection = db["faces"]


