import pickle
import face_recognition
import os
def load_images_and_encode_faces(directory='attendance_project/images', pickle_file='face_encodings.pkl'):
    """
    This function loads images from a specified directory, encodes the faces in the images,
    and saves/loads them from a pickle file to optimize repeated runs.

    Parameters:
    directory (str): The path to the directory containing the images. The default value is 'attendance_project/images'.
    pickle_file (str): The path to the pickle file where encodings will be stored or read from.

    Returns:
    tuple: A tuple containing two lists. The first list contains the known face encodings,
           and the second list contains the corresponding names of the faces.
    """
    if os.path.exists(pickle_file):
        # Load encodings from the pickle file if it exists
        with open(pickle_file, 'rb') as file:
            data = pickle.load(file)
            known_face_encodings = data['encodings']
            known_face_names = data['names']
            if __name__ == "__main__":
                print("Loaded face encodings from pickle file.")
    else:
        # Generate encodings and save them to the pickle file
        known_face_encodings = []
        known_face_names = []
        for filename in os.listdir(directory):
            if filename.endswith(".jpg") or filename.endswith(".jpeg"):
                path = os.path.join(directory, filename)
                face_image = face_recognition.load_image_file(path)
                face_encodings = face_recognition.face_encodings(face_image)
                if face_encodings:
                    face_encoding = face_encodings[0]
                    known_face_encodings.append(face_encoding)
                    known_face_names.append(os.path.splitext(filename)[0])

        # Save the encodings to the pickle file
        with open(pickle_file, 'wb') as file:
            data = {'encodings': known_face_encodings, 'names': known_face_names}
            pickle.dump(data, file)
            if __name__ == "__main__":
                print("Face encodings saved to pickle file.")

    return known_face_encodings, known_face_names


if __name__ == "__main__":
    load_images_and_encode_faces()