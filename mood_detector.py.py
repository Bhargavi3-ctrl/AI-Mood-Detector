import streamlit as st
from gtts import gTTS
import os
import speech_recognition as sr

# Function to detect mood
def detect_mood(text):
    text = text.lower()
    if "happy" in text or "good" in text:
        return "Happy 😄", "lightgreen"
    elif "sad" in text or "down" in text:
        return "Sad 😢", "lightblue"
    elif "angry" in text or "mad" in text:
        return "Angry 😡", "lightcoral"
    else:
        return "Neutral 🙂", "lightgray"

# Function to speak text using gTTS
def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("voice.mp3")
    audio_file = open("voice.mp3", "rb")
    st.audio(audio_file.read(), format="audio/mp3")

# Streamlit UI
st.set_page_config(page_title="Talking Mood Detector", layout="centered")

st.title("🎤 Talking Mood Detector AI")
st.write("👉 Type or Speak your mood, and I'll respond with color + voice!")

# Option to choose input type
choice = st.radio("How do you want to give input?", ["Text", "Voice 🎙️"])

user_input = ""

if choice == "Text":
    user_input = st.text_input("Type something about how you feel:")

elif choice == "Voice 🎙️":
    if st.button("🎙️ Start Recording"):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("Listening... Speak now!")
            audio = recognizer.listen(source, phrase_time_limit=5)
            try:
                user_input = recognizer.recognize_google(audio)
                st.success(f"You said: {user_input}")
            except:
                st.error("❌ Sorry, I couldn't understand. Try again!")

# Process mood
if user_input:
    mood, color = detect_mood(user_input)

    # Change background color
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {color} !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Show mood + voice response
    st.markdown(f"<h2 style='padding:10px'>{mood}</h2>", unsafe_allow_html=True)
    speak(f"Your mood is {mood}")
