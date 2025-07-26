
import os
from datetime import datetime

# Function to get the encodings of faces in a given folder
def get_face_encodings(photos):
    known_face_encodings = []
    known_face_names = []

    for file_name in os.listdir(photos):
        if file_name.endswith(('.jpg', '.jpeg', '.png')):