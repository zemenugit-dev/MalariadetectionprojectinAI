import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# ==========================================
# LOAD DATA
# ==========================================
print("\nLoading dataset...")

X = np.load("model/X.npy")
y = np.load("model/y.npy")

print("Dataset Loaded!")
print("X Shape:", X.shape)
print("Y Shape:", y.shape)

# ==========================================
# SPLIT DATA
# ==========================================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ==========================================
# DATA AUGMENTATION
# ==========================================
data_augmentation = tf.keras.Sequential([

    tf.keras.layers.RandomFlip("horizontal"),

    tf.keras.layers.RandomRotation(0.1),

    tf.keras.layers.RandomZoom(0.1),

])

# ==========================================
# BUILD STRONG CNN
# ==========================================
print("\nBuilding CNN Model...")

model = tf.keras.Sequential([

    tf.keras.Input(shape=(64,64,3)),

    data_augmentation,

    # BLOCK 1
    tf.keras.layers.Conv2D(
        32,
        (3,3),
        activation='relu',
        padding='same'
    ),

    tf.keras.layers.BatchNormalization(),

    tf.keras.layers.MaxPooling2D(2,2),

    # BLOCK 2
    tf.keras.layers.Conv2D(
        64,
        (3,3),
        activation='relu',
        padding='same'
    ),

    tf.keras.layers.BatchNormalization(),

    tf.keras.layers.MaxPooling2D(2,2),

    # BLOCK 3
    tf.keras.layers.Conv2D(
        128,
        (3,3),
        activation='relu',
        padding='same'
    ),

    tf.keras.layers.BatchNormalization(),

    tf.keras.layers.MaxPooling2D(2,2),

    # BLOCK 4
    tf.keras.layers.Conv2D(
        256,
        (3,3),
        activation='relu',
        padding='same'
    ),

    tf.keras.layers.BatchNormalization(),

    tf.keras.layers.MaxPooling2D(2,2),

    # FLATTEN
    tf.keras.layers.Flatten(),

    # DENSE
    tf.keras.layers.Dense(
        256,
        activation='relu'
    ),

    tf.keras.layers.Dropout(0.5),

    tf.keras.layers.Dense(
        128,
        activation='relu'
    ),

    tf.keras.layers.Dropout(0.3),

    # OUTPUT
    tf.keras.layers.Dense(
        1,
        activation='sigmoid'
    )

])

# ==========================================
# COMPILE MODEL
# ==========================================
model.compile(

    optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),

    loss='binary_crossentropy',

    metrics=['accuracy']

)

# ==========================================
# CALLBACKS
# ==========================================
early_stop = tf.keras.callbacks.EarlyStopping(

    monitor='val_loss',

    patience=5,

    restore_best_weights=True

)

reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(

    monitor='val_loss',

    factor=0.5,

    patience=2,

    verbose=1

)

# ==========================================
# TRAIN MODEL
# ==========================================
print("\nTraining Started...\n")

history = model.fit(

    X_train,
    y_train,

    validation_data=(X_test, y_test),

    epochs=20,

    batch_size=32,

    callbacks=[early_stop, reduce_lr],

    verbose=1

)

# ==========================================
# EVALUATE MODEL
# ==========================================
print("\nEvaluating Model...\n")

loss, accuracy = model.evaluate(X_test, y_test)

print(f"\nAccuracy: {accuracy:.4f}")

# ==========================================
# PREDICTIONS
# ==========================================
y_pred = model.predict(X_test)

y_pred = (y_pred > 0.5).astype(int)

# ==========================================
# REPORT
# ==========================================
print("\nClassification Report:\n")

print(classification_report(

    y_test,

    y_pred,

    labels=[0,1],

    target_names=[
        "Uninfected",
        "Parasitized"
    ]

))

# ==========================================
# SAVE MODEL
# ==========================================
model.save("model/malaria_model.keras")

print("\nModel Saved Successfully!")

# ==========================================
# PLOT RESULTS
# ==========================================
plt.figure(figsize=(12,5))

# Accuracy
plt.subplot(1,2,1)

plt.plot(history.history['accuracy'])

plt.plot(history.history['val_accuracy'])

plt.title("Accuracy")

plt.legend([
    "Train",
    "Validation"
])

# Loss
plt.subplot(1,2,2)

plt.plot(history.history['loss'])

plt.plot(history.history['val_loss'])

plt.title("Loss")

plt.legend([
    "Train",
    "Validation"
])

plt.tight_layout()

plt.show()