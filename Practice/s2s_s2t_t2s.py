import os
import wave
import numpy as np
import sounddevice as sd
import speech_recognition as sr
from gtts import gTTS
from datetime import datetime
import google.generativeai as genai

# ---------- Config ----------
SAMPLE_RATE = 16000
CHANNELS = 1
DTYPE = 'int16'
GOOGLE_API_KEY = "AIzaSyB-sys-YPEPBe1zOcMzSzk8kME6lcLcytU"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-flash")

# ---------- Folders ----------
os.makedirs("t2s_recordings", exist_ok=True)
os.makedirs("s2t_recordings", exist_ok=True)
os.makedirs("s2s_recordings", exist_ok=True)

# ---------- Helpers ----------
def timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def speak_text(text, filepath):
    tts = gTTS(text=text, lang='en')
    tts.save(filepath)
    print(f"[🔊] Speech saved to {filepath}")
    os.system(f"start {filepath}")

def record_audio(duration=5):
    print(f"[🎙️] Recording for {duration} seconds...")
    recording = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE,
                       channels=CHANNELS, dtype=DTYPE)
    sd.wait()
    return recording

def save_wav(filename, data):
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(data.tobytes())
    print(f"[💾] Audio saved to {filename}")

def transcribe_audio(filepath):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(filepath) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            print(f"[📝] Transcribed: {text}")
            return text
    except sr.UnknownValueError:
        return "[❌] Could not understand audio."
    except sr.RequestError as e:
        return f"[❌] API Error: {e}"

def ask_gemini(prompt):
    try:
        print("[🤖] Gemini generating reply...")
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"[❌] Gemini error: {e}"

# ---------- Features ----------
def text_to_speech():
    text = input("\n📝 Enter text to convert to speech: ").strip()
    ts = timestamp()
    audio_file = f"t2s_recordings/t2s_{ts}.mp3"
    text_file = f"t2s_recordings/t2s_{ts}.txt"

    speak_text(text, audio_file)
    with open(text_file, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"[✔] Text saved to {text_file}")

def speech_to_text():
    ts = timestamp()
    audio_file = f"s2t_recordings/s2t_{ts}.wav"
    text_file = f"s2t_recordings/s2t_{ts}.txt"

    recording = record_audio(5)
    save_wav(audio_file, recording)
    text = transcribe_audio(audio_file)
    with open(text_file, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"[✔] Transcription saved to {text_file}")

def speech_to_speech():
    ts = timestamp()
    input_audio = f"s2s_recordings/input_{ts}.wav"
    output_audio = f"s2s_recordings/response_{ts}.mp3"
    text_file = f"s2s_recordings/conversation_{ts}.txt"

    recording = record_audio(5)
    save_wav(input_audio, recording)
    user_text = transcribe_audio(input_audio)

    if user_text.startswith("[❌]"):
        print(user_text)
        return

    ai_reply = ask_gemini(user_text)
    speak_text(ai_reply, output_audio)

    with open(text_file, "w", encoding="utf-8") as f:
        f.write(f"👤 You said:\n{user_text}\n\n🤖 Gemini replied:\n{ai_reply}")
    print(f"[✔] Conversation saved to {text_file}")

# ---------- Main Menu ----------
def main():
    while True:
        print("\n===== AI Voice Assistant =====")
        print("1. Text to Speech")
        print("2. Speech to Text")
        print("3. Speech to Speech (with Gemini)")
        print("4. Exit")
        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            text_to_speech()
        elif choice == "2":
            speech_to_text()
        elif choice == "3":
            speech_to_speech()
        elif choice == "4":
            print("👋 Exiting...")
            break
        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    main()
