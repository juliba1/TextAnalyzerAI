# diagnosis:
    # 1 = melignant -> muss entfernt werden
    # 0 = benin -> muss nicht entfernt werden

import pandas as pd

dataset = pd.read_csv('../training_data/cancer.csv')

# y-Attribut -> melignant oder benin
# x-Attribut -> alle Features

x = dataset.drop(columns=["diagnosis(1=m, 0=b)"])
y = dataset["diagnosis(1=m, 0=b)"]

from sklearn.model_selection import train_test_split

# Test und Train Daten
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)  # Test = 20% von GrundInfos

import tensorflow as tf

model = tf.keras.models.Sequential()

model.add(tf.keras.layers.Dense(256, input_shape=(x_train.shape[1],), activation='sigmoid'))
model.add(tf.keras.layers.Dense(256, activation='sigmoid'))
model.add(tf.keras.layers.Dense(1, activation='sigmoid'))  # Output Layer

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

model.fit(x_train, y_train, epochs=1000)

model.evaluate(x_test, y_test)
