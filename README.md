# Keras Visualizer
![PyPI](https://img.shields.io/pypi/v/keras-visualizer) ![GitHub repo size](https://img.shields.io/github/repo-size/lordmahyar/keras-visualizer)

A Python Library for Visualizing Keras Models.

## New 2.4
> support `Dense`, `Conv2D`, `MaxPooling2D`, `Dropout`, `Flatten`, `Activation` layers.\
> added `Activation` info for Dense & Conv2D layers.\
> support view output file after visualizing.\

\
[Keras Visualizer on GitHub](https://github.com/lordmahyar/keras-visualizer)\
[Keras Visualizer on PyPI](https://pypi.org/project/keras-visualizer/)\
[Keras Visualizer on Libraries.io](https://libraries.io/pypi/keras-visualizer)

## Dependencies

* keras (or tensorflow v2)
* graphviz
```python
sudo pip3 install keras
sudo apt-get install graphviz && pip3 install graphviz
```

## Installation

### install
Use python package manager (pip) to install Keras Visualizer.
```bash
pip3 install keras-visualizer
```

### upgarde
Use python package manager (pip) to upgrade Keras Visualizer.
```bash
pip3 install keras-visualizer --upgrade
```

## Usage
#### import
```python
from keras_visualizer import visualizer
```
#### function
```python
visualizer(model) # save model
visualizer(model, format='png') # save both model & image file for visualizing model
visualizer(model, format='png', view=True) # open image file after visualization
```

## Documentation
```python
visualizer(model, filename='graph', format=None, view=False)
```

* `model` : a Keras model instance.
* `filename` : where to save the visualization.
* `format` : file format to save 'pdf', 'png'.
* `view` : open file after process if True.

> **Note :**\
> change `format='png'` or `format='pdf'` to save visualization file.\
> use `view=True` to open visualization file.
\
## Example
you can use simple examples in `examples` directory.

### Example 1 :
```python
from keras import models, layers  
from keras_visualizer import visualizer  
  
model = models.Sequential([  
    layers.Dense(64, activation='relu', input_shape=(8,)),  
    layers.Dense(6, activation='softmax'),  
    layers.Dense(32),  
    layers.Dense(9, activation='sigmoid')])  
  
visualizer(model, format='png', view=True)
```
![example 1](https://github.com/lordmahyar/keras_visualizer/blob/master/examples/example1_output.png)

---

### Example 2 :
```python
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
```
![example 2](https://github.com/lordmahyar/keras_visualizer/blob/master/examples/example2_output.png)
