from keras import models, layers
from keras_visualizer import visualizer

model = models.Sequential()
model.add(layers.Embedding(64, output_dim=256))
model.add(layers.LSTM(128))
model.add(layers.Dense(1, activation='sigmoid'))

visualizer(model, file_format='png', view=True)
