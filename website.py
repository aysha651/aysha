import streamlit as st
import speech_recognition as sr
import webbrowser
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

# Initialize the recognizer
recognizer = sr.Recognizer()

# Function to capture voice command
def capture_voice_command():
    with sr.Microphone() as source:
        st.write("Listening for command...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            st.write("You said: ", command)
            return command
        except sr.UnknownValueError:
            st.write("Sorry, I did not understand that.")
        except sr.RequestError:
            st.write("Could not request results; check your network connection.")
    return ""

# Function to open a website, play a video, or search content based on voice command
def handle_voice_command(command):
    if "open youtube" in command.lower():
        webbrowser.open("https://www.youtube.com")
        st.write("Opening YouTube...")
    elif "open chrome" in command.lower():
        webbrowser.open("https://www.google.com")
        st.write("Opening Google Chrome...")
    elif "explore" in command.lower() and "on youtube" in command.lower():
        search_query = command.lower().replace("play", "").replace("on youtube", "").strip()
        webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
        st.write(f"Searching for '{search_query}' on YouTube...")
    elif "explore" in command.lower():
        search_query = command.lower().replace("play", "").strip()
        webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
        st.write(f"Searching for '{search_query}' on YouTube...")
    elif "search" in command.lower() and "on google" in command.lower():
        search_query = command.lower().replace("search", "").replace("on google", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={search_query}")
        st.write(f"Searching for '{search_query}' on Google...")
    elif "search " in command.lower():
        search_query = command.lower().replace("search ", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={search_query}")
        st.write(f"Searching for '{search_query}' on Google...")
    else:
        st.write("No valid command detected.")

# Streamlit app interface
st.title("Voice-Controlled Browser Opener and Searcher")
st.write("Click the button below and give a voice command to open YouTube, open Chrome, (eg:explore tamil song, or search python).")

if st.button("Speak"):
    voice_command = capture_voice_command()
    if voice_command:
        handle_voice_command(voice_command)

