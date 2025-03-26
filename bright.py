import streamlit as st
import speech_recognition as sr
import screen_brightness_control as sbc
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

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Adjusting brightness. Say 'increase brightness', 'reduce brightness'")
        audio = recognizer.listen(source)
    
    try:
        command = recognizer.recognize_google(audio)
        st.write(f"Recognized command: {command}")
        return command.lower()
    except sr.UnknownValueError:
        st.write("Could not understand audio")
        return ""
    except sr.RequestError as e:
        st.write(f"Error with speech recognition service: {e}")
        return ""

def adjust_brightness(command):
    try:
        current_brightness = sbc.get_brightness(display=0)[0]  # Accessing the first element of the list
        if "increase brightness" in command:
            new_brightness = min(current_brightness + 10, 100)
            sbc.set_brightness(new_brightness)
            st.write(f"Brightness increased to {new_brightness}%")
        elif "reduce brightness" in command:
            new_brightness = max(current_brightness - 10, 0)
            sbc.set_brightness(new_brightness)
            st.write(f"Brightness decreased to {new_brightness}%")
        else:
            st.write("Command not recognized. Please say 'increase brightness' or 'decrease brightness'.")
    except Exception as e:
        st.write(f"Error adjusting brightness: {e}")


def main():
    st.title("Voice-Controlled Brightness Adjustment")
    st.write("______________________________________")
    
    if st.button("Speak"):
       command = recognize_speech()
       if "brightness" in command:
           adjust_brightness(command)
           
if __name__ == "__main__":
    main()
