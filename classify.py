import os
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model

def preprocess_image(image_path):
    image = Image.open(image_path).convert("L")
    image = image.resize((1000, 600))
    image_array = np.array(image) / 255.0
    image_array = image_array.reshape(1, 600, 1000, 1)
    return image_array

def classify_image(model, image_array):
    prediction = model.predict(image_array)
    predicted_class = np.argmax(prediction)
    predicted_proba = prediction[0][predicted_class]
    #print(f"Prediction in TensorFlow is: {predicted_class} with probability {predicted_proba}")
    return f"Down ({100*predicted_proba:.2f}%)" if predicted_class == 0 else f"Up ({100*predicted_proba:.2f}%)"

def main():
    model = load_model("ml/trend_classifier.h5")
    new_image_path = os.path.join("static", "images", "prod", "test.png")
    image_array = preprocess_image(new_image_path)
    predicted_class = classify_image(model, image_array)
    print(f"The predicted class for the new image is: {predicted_class}")

if __name__ == "__main__":
    main()