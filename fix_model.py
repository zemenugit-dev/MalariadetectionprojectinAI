import tensorflow as tf

# LOAD ORIGINAL MODEL
model = tf.keras.models.load_model(
    "model/malaria_model.keras",
    compile=False
)

# SAVE NEW CLEAN MODEL (still .keras)
model.save("model/malaria_model_fixed.keras")

print("Model fixed successfully")