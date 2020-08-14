from keras import models, layers
from keras_visualizer import visualizer

model = models.Sequential([
    layers.Dense(64, activation='relu', input_shape=(8,)),
    layers.Dense(6, activation='softmax'),
    layers.Dense(32),
    layers.Dense(9, activation='sigmoid')])

visualizer(model, format='png', view=True)
