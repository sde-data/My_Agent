import os
import numpy as np
import librosa
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Input
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

# ===============================
# 1️⃣ Load Dataset
# ===============================

DATA_PATH = "/home/sde/My_Agent/data"

X = []
y = []

for label, folder in enumerate(os.listdir(DATA_PATH)):
    folder_path = os.path.join(DATA_PATH, folder)

    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)

        # Load audio
        signal, sr = librosa.load(file_path, duration=2.5, sr=22050)

        # Extract MFCC features
        mfcc = librosa.feature.mfcc(y=signal, sr=sr, n_mfcc=40)
        mfcc_processed = np.mean(mfcc.T, axis=0)

        X.append(mfcc_processed)
        y.append(label)

X = np.array(X)
y = np.array(y)

# Convert labels to categorical
y = to_categorical(y)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ===============================
# 2️⃣ Build ANN Model
# ===============================

model = Sequential([
    Input(shape=(40,)),
    Dense(256, activation='relu'),
    Dropout(0.5),
    Dense(128, activation='relu'),
    Dense(y.shape[1], activation='softmax')
])

# ===============================
# 3️⃣ Compile Model
# ===============================

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# ===============================
# 4️⃣ Train Model
# ===============================

model.fit(
    X_train,
    y_train,
    epochs=50,
    batch_size=8,
    validation_data=(X_test, y_test)
)

# ===============================
# 5️⃣ Evaluate Model
# ===============================

loss, accuracy = model.evaluate(X_test, y_test)
print(f"\nTest Accuracy: {accuracy * 100:.2f}%")

# ===============================
# 6️⃣ Predict New Audio
# ===============================

test_file = "data/class0/class0_1.wav"  # change this
signal, sr = librosa.load(test_file, duration=2.5, sr=22050)
mfcc = librosa.feature.mfcc(y=signal, sr=sr, n_mfcc=40)
mfcc_processed = np.mean(mfcc.T, axis=0)
mfcc_processed = mfcc_processed.reshape(1, -1)

prediction = model.predict(mfcc_processed)
predicted_class = np.argmax(prediction)

print("Predicted Class:", predicted_class)