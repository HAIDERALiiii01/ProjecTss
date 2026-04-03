import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
import joblib


data = pd.read_csv("datasets.csv", header=None)
# print(data.head())

X = data.iloc[:, 1:]   # all columns except first
y = data.iloc[:, 0]    # first column (labels)

encoder = LabelEncoder()
y = encoder.fit_transform(y)

# print(encoder.classes_)  

X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.3, random_state=42, shuffle=True
)

X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.5, random_state=42, shuffle=True
)

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_val   = scaler.transform(X_val)
X_test  = scaler.transform(X_test)
joblib.dump(scaler, "scaler.pkl")

model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(182,)),

    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.4),

    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dropout(0.3),

    tf.keras.layers.Dense(len(encoder.classes_), activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

early_stop = tf.keras.callbacks.EarlyStopping(patience=5, restore_best_weights=True)

model.fit(
    X_train, y_train,
    epochs=40,
    validation_data=(X_val, y_val),
    callbacks=[early_stop]
)

loss, accuracy = model.evaluate(X_test, y_test)
print("Accuracy:", accuracy)

model.save("gesture_model.keras")
joblib.dump(encoder, "encoder.pkl")