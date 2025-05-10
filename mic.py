# mic.py
import speech_recognition as sr

def listen_for_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening... Speak now!")
        audio = r.listen(source, phrase_time_limit=5)
    try:
        command = r.recognize_google(audio)
        print(f"✅ You said: {command}")
        return command
    except sr.UnknownValueError:
        print("❌ Could not understand.")
        return None
    except sr.RequestError:
        print("⚠️ Speech recognition error.")
        return None
