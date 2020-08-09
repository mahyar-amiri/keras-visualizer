# Keras Visualizer

a python library for visualizing keras models.

## Dependencies

* keras
* graphviz
```python
pip3 install keras
pip3 install graphvis
```

## Installation

        
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Keras Visualizer.

```bash
pip3 install keras_visualizer
```

## Usage

```python
from keras_visualizer import visualizer

visualizer(model) # save model
visualizer(model, format='png') # save model and png file for visualizing model
```

## Parameters
```python
visualizer(model, filename='graph', title='Neural Network', format=None, view=False)
```

* model: a Keras model instance.
* filename: where to save the visualization.
* title: A title for the graph.
* format: file format to save 'pdf', 'png'.
* view: open file after process if True.

* change format to 'png' or 'pdf' to save visualization file

## Example
```python
from keras import models, layers
from keras_visualizer import visualizer

model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 3)),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(10, activation='relu'),
    layers.Dense(5, activation='softmax'),
    layers.Dense(7, activation='sigmoid')])

visualizer(model, format='png', view=True)
```
![graph](https://github.com/lordmahyar/keras_visualizer/blob/master/graph.png)

