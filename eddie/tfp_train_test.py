"""This creates and trains a model given some random data. It can be
used to test your installation of the relevant libraries.
"""

import numpy as np
import tensorflow as tf
import tensorflow_probability as tfp
# from tensorflow.keras import callbacks as cb

tfkl = tf.keras.layers
tfpl = tfp.layers
tfd = tfp.distributions
print("Loaded the libraries.")
print(tf.config.list_physical_devices())
MODEL_DIR = "./test_model/"

# Generate random data


data = np.load("data/training_data.npy")
print(data.shape)

print(data[:, 0:2, :].shape)


X = np.random.randn(500, 2)
Y = np.random.randn(500, 2)

# Make simple model

mirrored_strategy = tf.distribute.MirroredStrategy()
with mirrored_strategy.scope():
    model = tf.keras.Sequential(
         [tfkl.Dense(32, activation='tanh'),
         tfkl.Dense(2 * 6, activation=None),
         tfpl.MixtureSameFamily(2, tfpl.MultivariateNormalTriL(2))])

print("Built the model.")

# Train model

def nll(data_point, tf_distribution):
    """Negative log likelihood."""
    return -tf_distribution.log_prob(data_point)


LOSS = nll
BATCH_SIZE = 32
LEARNING_RATE = 1e-3
EPOCHS = 3
OPTIMISER = tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE)
VALIDATION_SPLIT = 0.2

model.compile(loss=LOSS, optimizer=OPTIMISER)

History = model.fit(
    X,
    Y,
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    shuffle=True,
    validation_split=VALIDATION_SPLIT,
    verbose=2,
)
print("Trained the model.")
