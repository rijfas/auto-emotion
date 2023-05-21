from flask import Flask, Response, render_template
from utils import generate_frames
from db import get_all_records

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/video_feed")
def video_feed():
    return Response(
        generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/result")
def result():
    records = get_all_records()
    return render_template("result.html", records=records)


if __name__ == "__main__":
    app.run(debug=True)
