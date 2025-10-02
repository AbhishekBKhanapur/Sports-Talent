import cv2
import mediapipe as mp
import streamlit as st
import time

mp_pose = mp.solutions.pose

def shuttle_live():
    cap = cv2.VideoCapture(0)
    laps = 0
    stage = None
    start_time = time.time()

    frame_placeholder = st.empty()
    stop_button = st.button("🛑 Stop Shuttle Run Test")

    with mp_pose.Pose(min_detection_confidence=0.5,
                      min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image)

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                hip_x = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x

                if hip_x < 0.3:
                    if stage != "left":
                        stage = "left"
                        laps += 1
                elif hip_x > 0.7:
                    if stage != "right":
                        stage = "right"
                        laps += 1

                elapsed = time.time() - start_time
                cv2.putText(image, f"Laps: {laps}", (10,40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
                cv2.putText(image, f"Time: {elapsed:.1f}s", (10,80),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

            frame_placeholder.image(image, channels="RGB")

            if stop_button:
                break

    cap.release()
    return laps, time.time() - start_time
