import numpy as np
import tensorflow as tf
import cv2

# ==========================================
# LOAD TRAINED MODEL
# ==========================================
print("Loading Prediction Model...")

model = tf.keras.models.load_model("model/malaria_model.keras")

print("Prediction Model Loaded Successfully!")

# ==========================================
# PREDICTION FUNCTION
# ==========================================
def predict_image(image_path):

    try:
        # Read image
        image = cv2.imread(image_path)

        # Check invalid image
        if image is None:
            return "Invalid Image", 0

        # Resize image
        image = cv2.resize(image, (64, 64))

        # Normalize image
        image = image.astype("float32") / 255.0

        # Add batch dimension
        image = np.expand_dims(image, axis=0)

        # ==========================================
        # MODEL PREDICTION
        # ==========================================
        prediction = model.predict(image, verbose=0)[0][0]

        # Convert to float
        prediction = float(prediction)

        # ==========================================
        # CLASSIFICATION LOGIC
        # ==========================================
        # IMPORTANT:
        # 0 = Parasitized
        # 1 = Uninfected
        # ==========================================

        if prediction >= 0.5:

            confidence = round(prediction * 100, 2)

            result = (
                f"Uninfected (Healthy) - "
                f"Confidence: {confidence}%"
            )

        else:

            confidence = round((1 - prediction) * 100, 2)

            result = (
                f"Parasitized (Malaria Detected) - "
                f"Confidence: {confidence}%"
            )

        # Return BOTH result and confidence
        return result, confidence

    except Exception as e:

        return f"Prediction Error: {str(e)}", 0