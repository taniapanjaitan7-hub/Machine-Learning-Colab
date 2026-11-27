
import argparse
import json
from pathlib import Path

import numpy as np
import tensorflow as tf


# ==================================================
# PROJECT CONFIGURATION
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "pakcoy_demo_3kelas.keras"

CLASS_PATH = BASE_DIR / "models" / "class_names_demo.json"

IMG_SIZE = (224, 224)


# ==================================================
# LOAD TRAINED MODEL
# ==================================================

def load_model():

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found: {MODEL_PATH}"
        )

    model = tf.keras.models.load_model(
        MODEL_PATH,
        compile=False
    )

    print("Model loaded successfully.")

    return model


# ==================================================
# LOAD CLASS LABELS
# ==================================================

def load_class_names():

    if not CLASS_PATH.exists():
        raise FileNotFoundError(
            f"Class labels not found: {CLASS_PATH}"
        )

    with open(
        CLASS_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        class_names = json.load(file)

    return class_names


# ==================================================
# IMAGE PREPROCESSING
# ==================================================

def prepare_image(image_path):

    image_path = Path(image_path)

    if not image_path.is_file():
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    image = tf.keras.utils.load_img(
        image_path,
        color_mode="rgb",
        target_size=IMG_SIZE
    )

    image_array = tf.keras.utils.img_to_array(
        image
    )

    image_array = np.expand_dims(
        image_array,
        axis=0
    )

    # MobileNetV2 preprocessing is already
    # included in the exported Keras model.

    return image_array


# ==================================================
# IMAGE CLASSIFICATION
# ==================================================

def predict_image(model, class_names, image_path):

    image_array = prepare_image(image_path)

    predictions = model.predict(
        image_array,
        verbose=0
    )[0]

    if len(predictions) != len(class_names):
        raise ValueError(
            "Model output and class labels do not match."
        )

    class_index = int(
        np.argmax(predictions)
    )

    confidence = float(
        predictions[class_index]
    ) * 100

    print("\n" + "=" * 50)
    print("PAKCOY CLASSIFICATION RESULT")
    print("=" * 50)

    print(f"Image      : {image_path}")
    print(f"Prediction : {class_names[class_index]}")
    print(f"Confidence : {confidence:.2f}%")

    print("\nCLASS PROBABILITIES")
    print("-" * 50)

    for name, probability in zip(
        class_names,
        predictions
    ):

        print(
            f"{name}: {probability * 100:.2f}%"
        )

    print("=" * 50)

    return class_names[class_index], confidence


# ==================================================
# MAIN PROGRAM
# ==================================================

def main():

    parser = argparse.ArgumentParser(
        description=(
            "Pakcoy Plant Classification "
            "Using MobileNetV2"
        )
    )

    parser.add_argument(
        "image",
        help="Path to the input Pakcoy image"
    )

    args = parser.parse_args()

    try:

        print("=" * 50)
        print("PAKCOY AGE CLASSIFICATION")
        print("MobileNetV2 Transfer Learning")
        print("=" * 50)

        model = load_model()

        class_names = load_class_names()

        predict_image(
            model,
            class_names,
            args.image
        )

    except Exception as error:

        print(f"\nError: {error}")
        raise SystemExit(1)


if __name__ == "__main__":

    main()
