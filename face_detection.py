import cv2
from time import sleep as wait
import face_recognition
import cv2
import os
import glob
import numpy as np
import sys

class SimpleFacerec:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []

        # Resize frame for a faster speed
        self.frame_resizing = 0.25

    def load_encoding_images(self, images_path):
        """
        Load encoding images from path
        :param images_path:
        :return:
        """
        i_path = images_path
        # Load Images
        images_path = glob.glob(os.path.join(images_path, "*.*"))
        total_img = len(images_path)
        print("{} encoding images found.".format(total_img))

        if total_img == 0:
            sys.exit(f"\nERROR: Either the '{i_path}' folder is empty or it is non existing, Please make one or add valid faces.\n     : Folder's name should be '{i_path[0:-1]}'\n")

        # Store image encoding and names
        for img_path in images_path:
            img = cv2.imread(img_path)
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Get the filename only from the initial file path.
            basename = os.path.basename(img_path)
            (filename, ext) = os.path.splitext(basename)
            # Get encoding
            img_encoding = face_recognition.face_encodings(rgb_img)[0]

            # Store file name and file encoding
            self.known_face_encodings.append(img_encoding)
            self.known_face_names.append(filename)
        print("Encoding images loaded")

    def detect_known_faces(self, frame):
        small_frame = cv2.resize(frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)
        # Find all the faces and face encodings in the current frame of video
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
            face_names.append(name)

        # Convert to numpy array to adjust coordinates with frame resizing quickly
        # face_locations = np.array(face_locations)
        # face_locations = face_locations / self.frame_resizing # face_locations.astype(int), 
        return face_names


# Encode faces from a folder
def init_dtct_face():
    sfr = SimpleFacerec()
    sfr.load_encoding_images("faces/")
    return sfr
    # Load Camera
def dtct_face(cap, sfr):


    print("checking...")
    ret, frame = cap.read()

        # Detect Faces
    face_names = sfr.detect_known_faces(frame)

    for name in face_names:
        if name == "Unknown":
            wait(2)
            pass

        else:
            in_front = name
            print("DEBUG: face of: ", name)
            while in_front == name:
                wait(2)
                ret, frame = cap.read()
                face_names = sfr.detect_known_faces(frame)
                for current_user in face_names:
                    if current_user == "Unknown":
                        print("there is no one in front or I don't know you")
                        return "no"
                    else:
                        in_front = current_user
                        return "yes"
    return "no"

def face(cap, sfr):
    global is_known_face
    is_known_face = True
    is_known_face = dtct_face(cap, sfr)


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    sfr = init_dtct_face()

    while True:
        face(cap, sfr)