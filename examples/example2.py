from keras import models
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Activation
from keras_visualizer import visualizer

model = models.Sequential()
model.add(Conv2D(64, (3, 3), input_shape=(28, 28, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(3))
model.add(Activation('sigmoid'))
model.add(Dense(1))

visualizer(model, format='png', view=True)