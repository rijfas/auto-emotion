from datetime import datetime
import cv2
from auto_emotion import detect_emotions
from db import get_db_connection

DETECTION_AGE = 5  # in seconds

camera = cv2.VideoCapture(0)


def get_duration_in_seconds(then, now):
    duration = now - then
    return duration.total_seconds()


def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            faces, image = detect_emotions(frame)
            conn = get_db_connection()
            for face in faces:
                if face["name"] != "Unknown" and face["emotion"]:
                    last_record = conn.execute(
                        "SELECT * FROM records ORDER BY created DESC LIMIT 1"
                    ).fetchone()
                    if (last_record == None) or (
                        get_duration_in_seconds(last_record["created"], datetime.now())
                        > DETECTION_AGE
                    ):
                        conn.execute(
                            "INSERT INTO records (created, name, emotion) VALUES (?, ?, ?)",
                            (datetime.now(), face["name"], face["emotion"]),
                        )
            conn.commit()
            conn.close()
            _, buffer = cv2.imencode(".jpg", image)
            frame = buffer.tobytes()
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")
