import os
import tensorflow as tf

# Get the absolute path to your project directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KERAS_MODEL_PATH = os.path.join(BASE_DIR, "model", "malaria_model.keras")
H5_MODEL_PATH = os.path.join(BASE_DIR, "model", "malaria_model.h5")

try:
    print("🔄 Loading the local Windows .keras model...")
    # Load without compiling to completely skip OS-specific layer configurations
    model = tf.keras.models.load_model(KERAS_MODEL_PATH, compile=False)
    
    print("💾 Saving model into highly compatible flat legacy .h5 format...")
    model.save(H5_MODEL_PATH)
    
    print("✅ SUCCESS! 'malaria_model.h5' has been generated in your model/ folder.")

except Exception as e:
    print(f"❌ Error during conversion: {str(e)}")