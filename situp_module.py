import cv2
import mediapipe as mp
import numpy as np
import streamlit as st

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

def situp_live():
    cap = cv2.VideoCapture(0)
    counter, stage = 0, None

    frame_placeholder = st.empty()
    stop_button = st.button("🛑 Stop Sit-up Test")

    with mp_pose.Pose(min_detection_confidence=0.5,
                      min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image)

            if results.pose_landmarks:
                lm = results.pose_landmarks.landmark
                hip = [lm[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                       lm[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                shoulder = [lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                            lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                knee = [lm[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                        lm[mp_pose.PoseLandmark.LEFT_KNEE.value].y]

                angle = calculate_angle(shoulder, hip, knee)

                if angle > 140:
                    stage = "down"
                if angle < 70 and stage == "down":
                    stage = "up"
                    counter += 1

                # Draw counter text on video
                cv2.putText(image, f"Sit-ups: {counter}", (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

                # Draw skeleton landmarks
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Show video feed with counter
            frame_placeholder.image(image, channels="RGB")

            if stop_button:
                break

    cap.release()
    return counter
