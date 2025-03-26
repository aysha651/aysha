import streamlit as st
import speech_recognition as sr
import pyttsx3
import datetime
import time
import threading
import pygame
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

# Initialize text-to-speech engine
engine = pyttsx3.init()

def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("please say('eg:set alarm 10.30 A.M')")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            st.write(f"Command received: {command}")
            return command.lower()
        except sr.UnknownValueError:
            st.write("Could not understand audio")
        except sr.RequestError:
            st.write("Could not request results; check your network connection")
    return None

def parse_time(command):
    try:
        if "set alarm" in command:
            time_part = command.split("set alarm ")[1]
            time_part = time_part.replace(".", "").replace("p.m", "PM").replace("a.m", "AM")
            alarm_time = datetime.datetime.strptime(time_part, "%I:%M %p").time()
            return alarm_time
    except IndexError:
        st.write("Invalid command format. Please say 'set alarm [time]'.")
    except ValueError:
        st.write("Invalid time format. Please say the time in 'HH:MM AM/PM' format.")
    return None

def set_alarm(command):
    alarm_time = parse_time(command)
    if alarm_time:
        try:
            current_time = datetime.datetime.now().time()
            st.write(f"Current time: {current_time.strftime('%I:%M %p')}")
            st.write(f"Alarm time: {alarm_time.strftime('%I:%M %p')}")

            current_datetime = datetime.datetime.combine(datetime.date.today(), current_time)
            alarm_datetime = datetime.datetime.combine(datetime.date.today(), alarm_time)
            if alarm_datetime < current_datetime:
                alarm_datetime += datetime.timedelta(days=1)

            time_difference = (alarm_datetime - current_datetime).total_seconds()
            if time_difference < 0:
                st.write("The specified time is in the past. Please set a future time.")
                return
            st.write(f"Alarm set for {alarm_time.strftime('%I:%M %p')}")
            alarm_thread = threading.Thread(target=alarm_ringtone, args=(time_difference,))
            alarm_thread.start()
        except Exception as e:
            st.write(f"Error setting alarm: {e}")

def alarm_ringtone(delay):
    time.sleep(delay)
    
    # Play the alarm sound using pygame
    pygame.mixer.init()
    # Update this path to the actual location of your audio file
    pygame.mixer.music.load('C:/Users/aysha/Downloads/australia-eas-alarm-267664.mp3')  
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(1)
    
    # Speak the wake-up message
    engine.say("Wake up! It's time!")
    engine.runAndWait()

st.title("Voice-Controlled Alarm Clock")
st.write("____________________________")

if st.button("Speak"):
    command = listen_for_command()
    if command:
        set_alarm(command)







