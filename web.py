import streamlit as st
import cv2
import speech_recognition as sr
from PIL import Image
from datetime import datetime
import os
import threading
import queue

st.title("Voice-Controlled Webcam")
st.write("_______________________")

# Queue to handle voice commands
command_queue = queue.Queue()
import base64


def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('img.jpg') 

def get_gallery_path():
    """Returns the default gallery path based on OS."""
    if os.name == 'nt':  # Windows
        return os.path.join(os.path.expanduser("/Users/aysha/OneDrive/Pictures/Saved Pictures"), "Pictures")
    else:  # Mac/Linux
        return os.path.join(os.path.expanduser("~"), "Pictures")

def listen_for_commands():
    """ Continuously listens for voice commands and adds them to a queue. """
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    while True:
        try:
            with microphone as source:
                st.write("Listening for commands...")
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio).lower()
                st.write(f"You said: {command}")
                command_queue.put(command)  # Add the command to the queue

        except sr.UnknownValueError:
            st.write("Sorry, I did not understand that.")
        except sr.RequestError:
            st.write("Could not request results from the speech recognition service.")
        except Exception as e:
            st.write(f"Error: {e}")

# Start the speech recognition in a separate thread
listener_thread = threading.Thread(target=listen_for_commands, daemon=True)
listener_thread.start()

camera_started = st.sidebar.checkbox("Start Camera", value=False)

frame_placeholder = st.empty()
captured_image_placeholder = st.empty()
cap = None

if camera_started:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("Error: Could not open webcam.")
    else:
        captured_image = None  # Store captured image
        gallery_path = get_gallery_path()  # Get system gallery path

        while camera_started:
            # Read and display webcam feed
            ret, frame = cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_placeholder.image(frame_rgb, caption='Webcam Feed', use_container_width=True)
            else:
                st.error("Error: Couldn't read frame.")
                break
            
            # Check for voice commands from the queue
            while not command_queue.empty():
                command = command_queue.get()

                if "capture image" in command:
                    captured_image = Image.fromarray(frame_rgb)
                    captured_image_placeholder.image(captured_image, caption='Captured Image', use_container_width=True)
                    st.sidebar.success("Image captured!")

                elif "save" in command:
                    if captured_image:
                        if not os.path.exists(gallery_path):
                            os.makedirs(gallery_path)  # Ensure gallery folder exists
                        file_path = os.path.join(gallery_path, f"captured_image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
                        captured_image.save(file_path)
                        st.sidebar.success(f"Image saved to gallery: {file_path} 🎉")
                    else:
                        st.write("No image to save. Please capture an image first.")

                elif "exit" in command:
                    st.write("Exiting...")
                    camera_started = False
                    break

        cap.release()
        frame_placeholder.empty()
        st.sidebar.write("Camera stopped.")

else:
    if cap is not None:
        cap.release()
    st.write("Camera is off.")
