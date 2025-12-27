from flask import Flask, request, send_from_directory, render_template
import os

app = Flask(__name__)

# Base music folder (update if needed)
BASE_PATH = r"C:\Users\Ashwa\Desktop\MoodMusic\music"
MOODS = ["happy", "sad", "angry", "neutral"]

# Ensure folders exist
for mood in MOODS:
    os.makedirs(os.path.join(BASE_PATH, mood), exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload/<mood>", methods=["POST"])
def upload_song(mood):
    if mood not in MOODS:
        return "Invalid mood", 400
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    save_path = os.path.join(BASE_PATH, mood, file.filename)
    file.save(save_path)
    return "Upload successful", 200

@app.route("/songs/<mood>/<filename>")
def serve_song(mood, filename):
    if mood not in MOODS:
        return "Invalid mood", 400
    folder = os.path.join(BASE_PATH, mood)
    return send_from_directory(folder, filename)

@app.route("/playlist/<mood>")
def get_playlist(mood):
    if mood not in MOODS:
        return "Invalid mood", 400
    folder = os.path.join(BASE_PATH, mood)
    songs = os.listdir(folder)
    return {"songs": songs}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

