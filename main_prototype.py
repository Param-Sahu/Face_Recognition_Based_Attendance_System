import cv2
import face_recognition
from face_encoding import load_images_and_encode_faces
import datetime
import gspread
from google.oauth2.service_account import Credentials

# Google Sheets setup
try:
    scope = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file('credentials.json', scopes=scope)
    client = gspread.authorize(creds)

    sheets_id = "your-google-sheets-id"
    workbook = client.open_by_key(sheets_id)

    # Create a new sheet for today's date if it doesn't exist
    today_date_str = datetime.datetime.now().strftime("%d-%m-%Y")
    try:
        sheet = workbook.worksheet(today_date_str)
    except gspread.exceptions.WorksheetNotFound:
        sheet = workbook.add_worksheet(title=today_date_str, rows="100", cols="20")
        sheet.append_row(["Name", "Timestamp"])

    online = True
except Exception as e:
    print("No Internet connection. Make sure you are connected to Internet.")
    online = False

# Load known faces
known_face_encodings, known_face_names = load_images_and_encode_faces()

# Function to check if attendance is already marked for the day for a student
def attendance_marked_today(student_name):
    if not online:
        return False

    records = sheet.get_all_records()
    today = datetime.datetime.now().date()
    for record in records:
        if record['Name'] == student_name:
            try:
                timestamp = datetime.datetime.strptime(record['Timestamp'], "%Y-%m-%d %H:%M:%S.%f")
                if timestamp.date() == today:
                    return True
            except (ValueError, TypeError):
                continue
    return False

# Open camera
video_capture = cv2.VideoCapture(0)

# Initialize loop variables
start_time = datetime.datetime.now()
duration_seconds = 25
end_time = start_time + datetime.timedelta(seconds=duration_seconds)

# Set to keep track of recorded faces
recorded_faces = set()

try:
    while datetime.datetime.now() < end_time and online: # Make sure you are connected to internet.
        # Capture frame-by-frame
        ret, frame = video_capture.read()
    
        # Check if the frame was captured successfully
        if not ret or frame is None:
            print("Error: Failed to capture frame. Exiting...")
            break

        # Resize frame to 1/4 size for faster processing
        try:
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        except Exception as e:
            print("Error while resizing frame:", e)
            break

        # Convert the image from BGR color to RGB color
        try:
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        except Exception as e:
            print("Error while converting color space:", e)
            break

        # Validate RGB frame
        if rgb_small_frame.dtype != 'uint8' or len(rgb_small_frame.shape) != 3:
            print(f"Error: RGB frame is invalid. Dtype: {rgb_small_frame.dtype}, Shape: {rgb_small_frame.shape}")
            break

        # Detect face locations in the RGB frame
        try:
            face_locations = face_recognition.face_locations(rgb_small_frame)
        except RuntimeError as e:
            print("RuntimeError while detecting face locations:", e)
            break
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []

        # Check if attendance is marked for the day for each recognized face
        for face_encoding in face_encodings:
            # Compare each face encoding to the known face encodings
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # If a match is found, use the name of the known face
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            face_names.append(name)

            # Update attendance if not already marked for the day
            if name != "Unknown" and name not in recorded_faces and not attendance_marked_today(name):
                recorded_faces.add(name)
                if online:
                    sheet.append_row([name, str(datetime.datetime.now())])

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations
            (top, right, bottom, left) = [value * 4 for value in (top, right, bottom, left)]

            # Draw a rectangle around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0,  255,0), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 2)

            # Display if attendance is already marked for the day
            if name != "Unknown" and attendance_marked_today(name):
                cv2.putText(frame, "Attendance has been Marked Today", (left + 6, bottom + 20), font, 0.5, (255, 0, 0), 1)

        cv2.imshow('Video', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Release the video capture object and close the OpenCV windows
    video_capture.release()
    cv2.destroyAllWindows()
