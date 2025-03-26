import streamlit as st
import subprocess

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
st.title("Control Me - Voice Assistance for System Controls")
st.write('------------------------------------------------')
st.title("Process Selector")

# Create a radio button for process selection
process = st.radio(
    "Select a process:",
    ("","Webcam Controller 🎥", "Volume Controller 🔊","Brightness Controller 🔆", "Alarm Controller ⏰", "Document Process 📝", "Calculator Process 🧮", "Website Process 🌍")
 )
st.write('------------------------------------------------')


# Display content based on the selected process
if process == "Webcam Controller 🎥":
    st.subheader("Webcam Controller")
    st.write("Here you can capture and save image.")
    # Add video processing functionality here
    subprocess.run(['streamlit','run','web.py'])
    
    
elif process == "Volume Controller 🔊":
    st.subheader("Volume Controller")
    st.write("Adjust and analyze volume levels.")
    # Add volume processing functionality here
    subprocess.run(['streamlit','run','volume.py'])
    

elif process == "Brightness Controller 🔆":
    st.subheader("Brightness Controller")
    st.write("Adjust and analyze brightness levels.")
    # Add brightness processing functionality here
    subprocess.run(['streamlit','run','bright.py'])



elif process == "Alarm Controller ⏰":
    st.subheader("Alarm Controller")
    st.write("Set and manage alarms.")
    # Add alarm processing functionality here
    subprocess.run(['streamlit', 'run', 'ala.py'])



elif process == "Document Process 📝":
    st.subheader("Document Process")
    st.write("Manage and manipulate documents.")
    # Add document processing functionality here
    subprocess.run(['streamlit','run','docu.py'])
    
    
    
elif process == "Calculator Process 🧮":
    st.subheader("Calculator Process")
    st.write("Perform various calculations.")
    # Add calculator functionality here
    subprocess.run(['streamlit','run','calcu.py'])



elif process == "Website Process 🌍":
    st.subheader("Website Process")
    st.write("Launch and manage website processes.")
    # Add website processing functionality here
    subprocess.run(['streamlit','run','website.py'])
    
    
