# main.py
import cv2
from gesture import GestureDetector
from mic import listen_for_command
from gpt import ask_gpt
from command import process_command_flow, is_awaiting_followup

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
                ask_gpt(command)
            print("\n--- Waiting for gesture ---\n")
        elif gesture == "OPEN":
            print("✋ Gesture detected! Status Report:")
            # Print the date, time, Location, and weather
        elif gesture == "POINT":
            print("👉 Gesture detected! Voice command mode:")
            user_input = listen_for_command()
            if user_input:
                response = process_command_flow(user_input)
                print(response)

                # 🔁 Check using function, not direct variable
                if is_awaiting_followup():
                    follow_up = listen_for_command()
                    if follow_up.lower() in ["cancel", "stop"]:
                        print("❌ Command cancelled.")
                    else:
                        print(process_command_flow(follow_up))


        elif gesture == "PEACE":
            print("✌️ Gesture detected! Peace out...")
            quit()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
