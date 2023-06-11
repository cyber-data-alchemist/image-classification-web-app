from flask import Flask, render_template, request, redirect, send_from_directory
from tensorflow.keras.models import load_model
from classify import preprocess_image, classify_image  # import the necessary functions
import os
import random
import sqlite3

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/images/prod"
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg"}

# Load the model when the app starts
model = load_model("ml/trend_classifier.h5")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/training", methods=["GET", "POST"])
def training():
    if request.method == "POST":
        image_name = request.form["image_name"]
        description = request.form["description"]

        conn = sqlite3.connect("db/image_descriptions.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO descriptions (image_name, description) VALUES (?, ?)", (image_name, description))
        conn.commit()
        conn.close()

    image_folder = os.path.join("static", "images", "training")
    random_image = random.choice(os.listdir(image_folder))
    image_path = os.path.join("images\\training", random_image)
    image_path = image_path.replace("\\", "/")

    return render_template("training.html", image_path=image_path)

@app.route("/test", methods=["GET", "POST"])
def test():
    if request.method == "POST":
        if 'image' not in request.files:
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file.filename = "test.png"  # rename the file to "test.png"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

            # Load the model here
            model = load_model("ml/trend_classifier.h5")

            # Preprocess the image and use the model to make a prediction
            image_array = preprocess_image(file_path)
            prediction = classify_image(model, image_array)

            return render_template('test.html', prediction=prediction, image_path=image_path)

    return render_template('test.html')


if __name__ == "__main__":
    app.run(debug=True)