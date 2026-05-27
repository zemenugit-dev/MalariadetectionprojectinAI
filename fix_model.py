import tensorflow as tf

# LOAD OLD MODEL
model = tf.keras.models.load_model(
    "model/malaria_model.keras",
    compile=False
)

# SAVE FIXED MODEL (NEW FILE)
model.save("model/malaria_model_fixed.keras")

print("Model fixed and saved!")