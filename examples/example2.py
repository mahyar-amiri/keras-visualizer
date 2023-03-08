from keras import models, layers
from keras_visualizer import visualizer

model = models.Sequential()
model.add(layers.Conv2D(64, (3, 3), input_shape=(28, 28, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Flatten())
model.add(layers.Dense(3))
model.add(layers.Dropout(0.5))
model.add(layers.Activation('sigmoid'))
model.add(layers.Dense(1))

visualizer(model, file_format='png', view=True)
