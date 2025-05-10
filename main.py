# main.py
import cv2
from gesture import GestureDetector
from mic import listen_for_command
from gpt import ask_gpt

def main():
    cam = cv2.VideoCapture(0)
    detector = GestureDetector()
    print("👋 Gesture-GPT is running. Show palm to activate.")
    
    while True:
        ret, frame = cam.read()
        if not ret:
            continue

        gesture = detector.detect_gesture(frame)
        if gesture == "FIST":
            print("✋ Gesture detected! Activating voice input...")
            command = listen_for_command()
            if command:
                response = ask_gpt(command)
                print("🤖 GPT-4 says:")
                print(response)
            print("\n--- Waiting for gesture ---\n")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
