# Face Recognition Attendance System
This project is a face recognition-based attendance system that uses OpenCV, face_recognition, and Google Sheets for recording attendance. 
The system captures video from the webcam, recognizes faces, and marks attendance to a Google Sheet. 
In the absence of an internet connection, it print a message indicating the lack of connectivity.

## Features 
- **Real-Time Face Recognition :** Captures video from the webcam and performs face recognition in real-time.
- **Face Encoding :** Encodes known faces from a specified directory.
- **Marks Attendance Automatically :** Logs the name and timestamp of recognized faces to a Google Sheet automatically.
- **Access Attendance Sheet on Desktop and Smartphone :** You can track real-time attendance in Google Sheet on `Desktop` as well as on your `Smartphone`.
- **Offline Handling :** Detects if there is no internet connection and prints a message "No internet connection." and stop the program.
- **Daily Logs :** Creates a new sheet in the Google Sheets document for each day, organizing attendance records by date.

## Installation
1. **Clone the Repository :**
```bash
git clone https://github.com/Future-Quantum/attendance.git    
```
2. **Install Dependencies :**
- OpenCV and Face_Recognition : 
```bash
pip install opencv-python face-recognition 
```
- Install Google Sheet API in Python
  - For Windows
  ```bash
  pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib gspread
  ```
  - For Mac
  ```bash
  pip3 install google-api-python-client google-auth-httplib2 google-auth-oauthlib gspread
  ```
3. **Set Up Google Sheets API :** Save the `credentials.json` file in the project directory (i.e. In the same folder where `main.py` is saved).
4. **Prepare Images :** Make sure images of known individuals should be in the `attendance_project/images` directory.
5. **Internet Connection :** Make sure you are connected to internet to run this program smoothly.

## Functionality 

- The script will open the webcam and start capturing frames.
- It will attempt to recognize faces from the frames.
- If a face is recognized and attendance for the day is not already marked, it will log the name and timestamp in the Google Sheets document.
- If there is no internet connection, it will print "No internet connection." and stop the program.

## How It Works
Loading and Encoding Faces :
- The `load_images_and_encode_faces` function loads face images from the specified directory and encodes them using the `face_recognition` library.

Google Sheets Setup :
- The script uses the `gspread` library to connect to Google Sheets using the provided service account credentials.
- It creates a new sheet for the current date if it doesn't already exist.

Face Recognition and Attendance Logging :
- The webcam captures frames which are processed to detect and recognize faces.
- Recognized faces are checked against the attendance log for the day.
- If a face is recognized and attendance is not already marked, the name and timestamp are logged in the Google Sheets document.

## Notes
- Ensure the Google Sheets API is enabled for your Google Cloud project and the service account has edit access to the Google Sheets document.
- You can configure the script to run for a different duration or adjust other parameters as needed.


## Attendance Sheet can be accessed on desktop as well as on smartphone with automatic updation
- ### Attendance Sheet on 07-06-2024 
  ![image](https://github.com/user-attachments/assets/180d2f06-c084-497c-9636-b89a4e1ece30)

- ### Attendance Sheet on 08-06-2024
  ![image](https://github.com/user-attachments/assets/84875177-e77d-4ac9-a02b-ed2605dbe634)


