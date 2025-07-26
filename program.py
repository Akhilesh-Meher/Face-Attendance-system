import cv2
import face_recognition
import os
from datetime import datetime

# Function to get the encodings of faces in a given folder
def get_face_encodings(photos):
    known_face_encodings = []
    known_face_names = []

    for file_name in os.listdir(photos):
        if file_name.endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(photos, file_name)
            image = face_recognition.load_image_file(image_path)
            face_encoding = face_recognition.face_encodings(image)[0]
            known_face_encodings.append(face_encoding)
            known_face_names.append(os.path.splitext(file_name)[0])

    return known_face_encodings, known_face_names

# Function to mark attendance
def mark_attendance(name):
    with open('attendance_log.txt', 'a') as file:
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{name} - {timestamp}\n")

# Main function for face recognition and attendance tracking
def main():
    images_folder = (r'D:\FACE ATTENDANCE SYSTEM\photos')
    video_capture = cv2.VideoCapture(0)

    known_face_encodings, known_face_names = get_face_encodings(images_folder)

    while True:
        ret, frame = video_capture.read()

        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

            if name != "Unknown":
                mark_attendance(name)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        if cv2.waitKey(1) & 0xFF == ord('Q'):
            break
        
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
