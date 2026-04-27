from dotenv import load_dotenv
load_dotenv()

import cv2
import os
from test_sms import send_sms
import cv2
import os
from test_sms import send_sms

def detect_vehicle(video_path):
    cap = cv2.VideoCapture(video_path)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 👇 Your detection logic here
        # Example placeholder:
        vehicle_detected = True  # Replace with your real model logic

        if vehicle_detected:
            print("🚗 No Parking Violation Detected")

            # Example phone number (replace with DB value later)
            owner_number = "+91XXXXXXXXXX"

            message = "🚫 Your vehicle is parked in a NO PARKING zone. Fine applied."

            send_sms(owner_number, message)

            break

        cv2.imshow("Frame", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    detect_vehicle("test.mp4")