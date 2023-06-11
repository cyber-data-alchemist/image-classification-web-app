import os
import sqlite3
import numpy as np
from PIL import Image
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras import layers, models
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

def load_data_from_db():
    conn = sqlite3.connect("db/image_descriptions.db")
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT image_name, description FROM descriptions")
    data = cursor.fetchall()
    conn.close()
    return data

def load_images_and_labels(data, img_folder):
    images = []
    labels = []
    for image_name, label in data:
        image_path = os.path.join(img_folder, image_name)
        image = Image.open(image_path).convert("L")
        image = image.resize((1000, 600))
        image_array = np.array(image) / 255.0
        images.append(image_array)
        labels.append(label)

    return np.array(images), np.array(labels)

def create_model(input_shape):
    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(128, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(128, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Flatten())
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(2, activation='softmax'))
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

def main():
    data = load_data_from_db()
    img_folder = 'static'
    images, labels = load_images_and_labels(data, img_folder)

    le = LabelEncoder()
    labels = le.fit_transform(labels)
    labels = to_categorical(labels, num_classes=2)

    X_train, X_val, y_train, y_val = train_test_split(images, labels, test_size=0.2, random_state=42)
    X_train = X_train.reshape(-1, 600, 1000, 1)
    X_val = X_val.reshape(-1, 600, 1000, 1)

    input_shape = (600, 1000, 1)
    model = create_model(input_shape)

    callbacks = [EarlyStopping(patience=10, restore_best_weights=True),
                 ModelCheckpoint('ml/best_model.h5', save_best_only=True)]

    model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=100, batch_size=32, callbacks=callbacks)

    model.save("ml/trend_classifier.h5")

if __name__ == "__main__":
    main()