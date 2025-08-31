from gtts import gTTS
import os

# Create output folder
OUTPUT_FOLDER = "t2s_recording"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def save_text_to_file(text, filename="saved_text.txt"):
    filepath = os.path.join(OUTPUT_FOLDER, filename)
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(text)
    print(f"[✔] Text saved to '{filepath}'")
    return filepath

def convert_text_to_speech(text, mp3_file="saved_speech.mp3", lang="en"):
    filepath = os.path.join(OUTPUT_FOLDER, mp3_file)
    tts = gTTS(text=text, lang=lang)
    tts.save(filepath)
    print(f"[✔] Speech saved to '{filepath}'")
    return filepath

def play_audio_windows(mp3_file):
    if os.path.exists(mp3_file):
        print(f"[▶] Playing: {mp3_file}")
        os.system(f'start {mp3_file}')  # Windows only
    else:
        print("[✘] Audio file not found!")

def main():
    print("🔊 Google Text-to-Speech (Python 3.13 Safe Version)\n")
    user_text = input("Enter the text to convert to speech: ").strip()

    text_file = save_text_to_file(user_text)
    audio_file = convert_text_to_speech(user_text)

    play_choice = input("Do you want to play the audio? (y/n): ").strip().lower()
    if play_choice == 'y':
        play_audio_windows(audio_file)

    print("\n✅ Done!")

if __name__ == "__main__":
    main()
