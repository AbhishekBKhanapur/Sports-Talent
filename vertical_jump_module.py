import cv2
import mediapipe as mp
import streamlit as st

mp_pose = mp.solutions.pose

def jump_live():
    cap = cv2.VideoCapture(0)
    max_jump = 0
    base_y = None

    frame_placeholder = st.empty()
    stop_button = st.button("🛑 Stop Vertical Jump Test")

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
                hip_y = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y

                if base_y is None:
                    base_y = hip_y

                jump_height = (base_y - hip_y) * 100
                if jump_height > max_jump:
                    max_jump = jump_height

                cv2.putText(image, f"Jump Height: {jump_height:.1f}", (10, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
                cv2.putText(image, f"Max Jump: {max_jump:.1f}", (10, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

            frame_placeholder.image(image, channels="RGB")

            if stop_button:
                break

    cap.release()
    return max_jump
