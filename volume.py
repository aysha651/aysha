import streamlit as st
import speech_recognition as sr
import pyautogui
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


def adjust_volume(command):
    if command == 'increase volume':
        st.write("increasing volume...")
        pyautogui.press("volumeup")
    elif command == 'decrease volume':
       st.write("decreasing volume...")
       pyautogui.press("volumedown")
    elif command == 'mute':
        st.write("muting volume...")
        pyautogui.press("volumemute")
    elif command == 'unmute':
        st.write("unmuting volume...")
        pyautogui.press("volumemute")

def recognize_speech():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        st.write("Please say a command: 'increase volume', 'decrease volume', 'mute', or 'unmute'")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            st.write(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            st.write("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            st.write("Sorry, my speech service is down.")
            return ""

st.title("Voice-Controlled Volume Adjustment")
st.write("__________________________________")

if st.button('Speak'):
    command = recognize_speech()
    if command in ['increase volume', 'decrease volume', 'mute', 'unmute']:
        adjust_volume(command)
        st.write(f"Executed command: {command}")
    else:
        st.write("Invalid command")
