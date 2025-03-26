import streamlit as st
import speech_recognition as sr
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
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Please say a calculation (e.g., 'two plus two')")
        audio = r.listen(source)

        try:
            text = r.recognize_google(audio)
            st.success(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            st.error("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError:
            st.error("Could not request results from Google Speech Recognition service.")
            return None
def calculate(command):
    try:
        st.write(f"Received command: {command}")
        command = command.lower().strip()

        # Add debug statements to check if replacements are happening
        st.write(f"Initial command: {command}")

        # Replace keywords with mathematical operators
        command = command.replace('plus', '+')
        command = command.replace('minus', '-')
        command = command.replace('multiply', '*').replace('x', '*')
        command = command.replace('divide', '/')

        st.write(f"Modified command: {command}")

        # Evaluate the modified command
        result = eval(command)
        st.write(f"Result: {result}")

    except Exception as e:
        st.write(f"Error in calculation: {e}")

def main():
    st.title("Voice-Controlled Calculator")
    st.write("___________________________")

    if st.button("begin"):
        command = recognize_speech()
        if command:
            st.write(f"Original command: {command}")
            calculate(command)

if __name__ == "__main__":
    main()


