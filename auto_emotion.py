import pickle
from collections import Counter
from pathlib import Path

import face_recognition
from PIL import Image, ImageDraw
from fer import FER
import numpy as np

BOX_COLOR = "blue"
TEXT_COLOR = "white"


encodings_file = Path("output/encodings.pkl")
emotion_detector = FER(mtcnn=True)


def train():
    names = []
    encodings = []

    for filepath in Path("training").glob("*/*"):
        name = filepath.parent.name
        image = face_recognition.load_image_file(filepath)

        face_locations = face_recognition.face_locations(image, model="hog")
        face_encodings = face_recognition.face_encodings(image, face_locations)

        for encoding in face_encodings:
            names.append(name)
            encodings.append(encoding)

    name_encodings = {"names": names, "encodings": encodings}
    with encodings_file.open(mode="wb") as f:
        pickle.dump(name_encodings, f)


def detect_emotions(image_location):
    with encodings_file.open(mode="rb") as f:
        loaded_encodings = pickle.load(f)

    input_image = image_location

    input_face_locations = face_recognition.face_locations(input_image, model="hog")
    input_face_encodings = face_recognition.face_encodings(
        input_image, input_face_locations
    )

    pillow_image = Image.fromarray(input_image)
    draw = ImageDraw.Draw(pillow_image)
    faces = []

    for bounding_box, unknown_encoding in zip(
        input_face_locations, input_face_encodings
    ):
        name = _detect_face(unknown_encoding, loaded_encodings)
        if not name:
            name = "Unknown"
        top, right, bottom, left = bounding_box
        cropped_image = np.array(pillow_image.crop(box=(left, top, right, bottom)))
        emotion, _ = emotion_detector.top_emotion(cropped_image)
        _display_caption(draw, bounding_box, f"{name}:{emotion}")
        faces.append({"name": name, "emotion": emotion})

    del draw
    return faces, np.array(pillow_image)


def _detect_face(unknown_encoding, loaded_encodings):
    boolean_matches = face_recognition.compare_faces(
        loaded_encodings["encodings"], unknown_encoding
    )
    votes = Counter(
        name for match, name in zip(boolean_matches, loaded_encodings["names"]) if match
    )
    if votes:
        return votes.most_common(1)[0][0]


def _display_caption(draw, bounding_box, caption):
    top, right, bottom, left = bounding_box
    draw.rectangle(((left, top), (right, bottom)), outline=BOX_COLOR)
    text_left, text_top, text_right, text_bottom = draw.textbbox(
        (left, bottom), caption
    )
    draw.rectangle(
        ((text_left, text_top), (text_right, text_bottom)),
        fill=BOX_COLOR,
        outline=BOX_COLOR,
    )
    draw.text(
        (text_left, text_top),
        caption,
        fill=TEXT_COLOR,
    )


if __name__ == "__main__":
    print("Info: Training the model")
    train()
    print("Success: Training completed")
