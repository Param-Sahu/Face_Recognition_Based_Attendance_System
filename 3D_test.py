import cv2
import mediapipe as mp
import numpy as np
import time

# Eye indices based on Mediapipe's Face Mesh
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

# EAR calculation
def calculate_ear(eye):
    A = np.linalg.norm(np.array(eye[1]) - np.array(eye[5]))
    B = np.linalg.norm(np.array(eye[2]) - np.array(eye[4]))
    C = np.linalg.norm(np.array(eye[0]) - np.array(eye[3]))
    ear = (A + B) / (2.0 * C)
    return ear

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

cap = cv2.VideoCapture(0)
blink_count = 0
blink_detected = False
ear_threshold = 0.21
consecutive_frames = 2
frame_counter = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb)

    if result.multi_face_landmarks:
        for face_landmarks in result.multi_face_landmarks:
            landmarks = face_landmarks.landmark
            left_eye = [(int(landmarks[i].x * w), int(landmarks[i].y * h)) for i in LEFT_EYE]
            right_eye = [(int(landmarks[i].x * w), int(landmarks[i].y * h)) for i in RIGHT_EYE]

            left_ear = calculate_ear(left_eye)
            right_ear = calculate_ear(right_eye)
            avg_ear = (left_ear + right_ear) / 2.0

            # Draw eye landmarks
            for pt in left_eye + right_eye:
                cv2.circle(frame, pt, 2, (0, 255, 0), -1)

            if avg_ear < ear_threshold:
                frame_counter += 1
            else:
                if frame_counter >= consecutive_frames:
                    blink_count += 1
                    blink_detected = True
                frame_counter = 0

            status = "Live Face Detected" if blink_detected else "No Blink - Possibly Fake"
            color = (0, 255, 0) if blink_detected else (0, 0, 255)
            cv2.putText(frame, f"{status}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            cv2.putText(frame, f"Blinks: {blink_count}", (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

    cv2.imshow("Blink-Based Liveness Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
