import cv2
import torch
import threading
import queue
import time
import smtplib
from email.message import EmailMessage
from ultralytics import YOLO
import os
from playsound import playsound

# ================================
# CONFIGURATION
# ================================

PHONE_CAMERA_URL = 0     
MODEL_NAME = "yolov8n.pt"

EMAIL_SENDER =  os.getenv("EMAIL_SENDER") #"harinivaradaraju71@gmail.com"
EMAIL_PASSWORD =  os.getenv("EMAIL_PASSWORD") #"lkshalohjijopxpu"
EMAIL_RECEIVER =  os.getenv("EMAIL_RECEIVER") #"harinivaradaraju71@gmail.com"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

CONF_THRESHOLD = 0.6
EMAIL_COOLDOWN = 30

ALARM_SOUND = "alarm.mp3"

# ================================
# LOAD YOLO MODEL
# ================================

model = YOLO(MODEL_NAME)

# ================================
# GPU / CPU SELECTION
# ================================

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

print("Running on:", device)

# ================================
# FRAME QUEUE
# ================================

frame_queue = queue.Queue(maxsize=5)

# ================================
# EMAIL FUNCTION
# ================================

def send_email(image_path):
    try:
        msg = EmailMessage()
        msg["Subject"] = "⚠ Intrusion Alert"
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER

        msg.set_content("A person was detected in the monitored area.")

        with open(image_path, "rb") as f:
            img = f.read()

        msg.add_attachment(img, maintype="image", subtype="jpeg", filename="intruder.jpg")

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)

        print("Email sent!")

    except Exception as e:
        print("Email failed:", e)

# ================================
# ALARM FUNCTION
# ================================

def play_alarm():
    try:
        if os.path.exists(ALARM_SOUND):
            playsound(ALARM_SOUND)
        else:
            print("Alarm file not found!")
    except Exception as e:
        print("Alarm error:", e)

# ================================
# CAMERA CAPTURE THREAD
# ================================

def capture_frames():

    cap = cv2.VideoCapture(PHONE_CAMERA_URL)

    while True:

        ret, frame = cap.read()

        if not ret:
            continue

        if not frame_queue.full():
            frame_queue.put(frame)

# ================================
# PERSON DETECTION THREAD
# ================================

last_email_time = 0

def detect_person():

    global last_email_time

    while True:

        frame = frame_queue.get()

        results = model(frame, device=device)

        detected = False

        for r in results:
            for box in r.boxes:

                cls = int(box.cls[0])
                conf = float(box.conf[0])

                if model.names[cls] == "person" and conf > CONF_THRESHOLD:

                    detected = True

                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)

                    cv2.putText(frame, "PERSON",
                                (x1, y1-10),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.6,
                                (0,255,0),
                                2)

        # SEND EMAIL + PLAY ALARM
        if detected and time.time() - last_email_time > EMAIL_COOLDOWN:

            filename = "intruder.jpg"
            cv2.imwrite(filename, frame)

            threading.Thread(target=send_email, args=(filename,), daemon=True).start()
            threading.Thread(target=play_alarm, daemon=True).start()

            last_email_time = time.time()

        cv2.imshow("Intrusion Monitor", frame)

        if cv2.waitKey(1) == 27:
            break

# ================================
# MAIN
# ================================

if __name__ == "__main__":

    t1 = threading.Thread(target=capture_frames)
    t2 = threading.Thread(target=detect_person)

    t1.daemon = True
    t2.daemon = True

    t1.start()
    t2.start()

    while True:
        time.sleep(1)