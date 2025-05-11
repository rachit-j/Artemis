# mic.py
import speech_recognition as sr

def listen_for_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening... Speak now.")
        r.adjust_for_ambient_noise(source, duration=0.5)  # Optional: better in noisy rooms
        try:
            audio = r.listen(source)  # Waits until silence is detected
            command = r.recognize_google(audio)
            print(f"✅ You said: {command}")
            return command
        except sr.UnknownValueError:
            print("❌ Could not understand.")
            return None
        except sr.RequestError:
            print("⚠️ Speech recognition service error.")
            return None
