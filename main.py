import cv2
import mediapipe as mp
import pyautogui
import streamlit as st

# Setup OpenCV, Mediapipe, and PyAutoGUI
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
hand_detector = mp.solutions.hands.Hands(max_num_hands=1)
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
index_y = 0

# Streamlit App
st.title("Virtual Mouse using Streamlit")

# Function to control the virtual mouse
def control_virtual_mouse(frame):
    global index_y
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks
    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                if id == 8:
                    index_x = screen_width / frame_width * x
                    index_y = screen_height / frame_height * y
                if id == 4:
                    thumb_x = screen_width / frame_width * x
                    thumb_y = screen_height / frame_height * y
                    if abs(index_y - thumb_y) < 50:
                        pyautogui.click()
                        pyautogui.sleep(1)
                    elif abs(index_y - thumb_y) < 100:
                        pyautogui.moveTo(index_x, index_y)

# Streamlit main app
with st.spinner("Loading..."):
    while True:
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        control_virtual_mouse(frame)
        st.image(frame, channels="BGR", use_column_width=True)
