"""
Script for constructing and training MDN model of transition density.
"""

import pickle
from pathlib import Path
import numpy as np
import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow.keras import callbacks as cb
from preprocessing import Scaler, load_training_data, transform_to_dx

tfkl = tf.keras.layers
tfpl = tfp.layers
tfd = tfp.distributions
kl = tfd.kullback_leibler
tf.keras.backend.set_floatx("float64")

print("Loaded the libraries.")
print(tf.config.list_physical_devices())

# Model hyperparameters

# 15 here comes from the number of alphas, the number of mu's and the entries of the covariance matrix.
N_C = 15
DT = 4

MODEL_DIR = (f"models/james/GDP_{DT:.0f}day_NC{N_C}/")

if not Path(MODEL_DIR).exists():
    Path(MODEL_DIR).mkdir(parents=True)


# --- PREPARE DATA ---

DATA_DIR = "data/"
DATA_FILE = "training_data.npy"
# DATA_DIR = f"data/GDP/{DT:.0f}day/"

data = load_training_data(DATA_DIR + DATA_FILE, N=1000000)  
N = data.shape[0]
print(f"Loaded {N = } datapoints")

data = transform_to_dx(data)

X = data[:, 0:2, :].reshape(N, 4)
Y = data[:, 2:4, :].reshape(N, 4)

# Xws = X.copy()
# Xws[:, 0] -= 360.0
# Xes = X.copy()
# Xes[:, 0] += 360.0

# Periodicising X0.
# X = np.concatenate((X, Xes, Xws), axis=0)
# Y = np.concatenate((Y, Y, Y), axis=0)

Xscaler = Scaler(X)
Yscaler = Scaler(Y)

X_ = Xscaler.standardise(X)
Y_ = Yscaler.standardise(Y)
del X, Y

with open(MODEL_DIR + r"Xscaler.pkl", "wb") as file:
    pickle.dump(Xscaler, file)

with open(MODEL_DIR + r"Yscaler.pkl", "wb") as file:
    pickle.dump(Yscaler, file)

# --- BUILD MODEL ---

mirrored_strategy = tf.distribute.MirroredStrategy()
with mirrored_strategy.scope():
    model = tf.keras.Sequential(
        [tfkl.Dense(256, activation='tanh'),
         tfkl.Dense(256, activation='tanh'),
         tfkl.Dense(256, activation='tanh'),
         tfkl.Dense(256, activation='tanh'),
         tfkl.Dense(512, activation='tanh'),
         tfkl.Dense(512, activation='tanh'),
         tfkl.Dense(N_C * 2, activation=None),
         tfpl.MixtureSameFamily(2, tfpl.MultivariateNormalTriL(4))])

print("Built the model.")

# --- TRAIN MODEL ---

LOG_FILE = "log.csv"
CHECKPOINT_FILE = "checkpoint_epoch_{epoch:02d}/weights"
TRAINED_FILE = "trained/weights"

# Training configuration


def nll(data_point, tf_distribution):
    """Negative log likelihood."""
    return -tf_distribution.log_prob(data_point)


LOSS = nll
BATCH_SIZE = 8192
LEARNING_RATE = 5e-5
EPOCHS = 10000
# EPOCHS = 100000
OPTIMISER = tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE)
VALIDATION_SPLIT = 0.2

# Callbacks
CSV_LOGGER = cb.CSVLogger(MODEL_DIR + LOG_FILE)
BATCHES_PER_EPOCH = int(
    np.ceil(X_.shape[0] / BATCH_SIZE * (1 - VALIDATION_SPLIT)))
CHECKPOINTING = cb.ModelCheckpoint(
    MODEL_DIR + CHECKPOINT_FILE,
    save_freq=10 * BATCHES_PER_EPOCH,
    verbose=1,
    save_weights_only=True)
EARLY_STOPPING = cb.EarlyStopping(monitor="val_loss",
                                  patience=50, min_delta=0.0)
CALLBACKS = [CHECKPOINTING, CSV_LOGGER, EARLY_STOPPING]

# Model compilation and training
model.compile(loss=LOSS, optimizer=OPTIMISER)

History = model.fit(
    X_,
    Y_,
    epochs=EPOCHS,
    callbacks=CALLBACKS,
    batch_size=BATCH_SIZE,
    shuffle=True,
    validation_split=VALIDATION_SPLIT,
    verbose=2,
)

model.save_weights(MODEL_DIR + TRAINED_FILE)

print("Trained the model.")
