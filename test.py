'''
    Test file for checking the face recognition library,
    image data type,shpae and RGB format for face_encodings function to work properly.
'''
import cv2
import numpy as np
import face_recognition

# Load the image
image_path = "attendance_project/images/Param_Sahu.jpg"
image = cv2.imread(image_path)

# Check if the image is loaded properly
if image is None:
    print("Error: Unable to load image.")
else:
    print("Image loaded successfully.")
    print(f"Image shape: {image.shape}")  # Check shape
    print(f"Data type: {image.dtype}")  # Check data type

    # Convert BGR to RGB
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    print(f"Converted Image shape: {rgb_image.shape}")
    print(f"Converted Data type: {rgb_image.dtype}")

    # Check the range of pixel values (should be 0-255 for 8-bit)
    print(f"Pixel value range: Min={np.min(rgb_image)}, Max={np.max(rgb_image)}")

    # Try detecting face locations
    
    face_locations = face_recognition.face_locations(rgb_image)
    print("Detected face locations:", face_locations)
    
