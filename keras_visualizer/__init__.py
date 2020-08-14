"""
Copyright (C) 2020 by Mahyar Amiri

Permission is hereby granted, free of charge,
to any person obtaining a copy of this software and associated
documentation files (the 'Software'),
to deal in the Software without restriction,
including without l> imitation the rights to
use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice
shall be included in all copies or substantial portions of the Software.
"""


def visualizer(model, filename='graph', format=None, view=False):
    """Visualize a Sequential model.

    # Arguments

        model: a Keras model instance.

        filename: where to save the visualization.

        format: file format to save 'pdf', 'png'.

        view: open file after process if True.

    * change format to 'png' or 'pdf' to save visualization file
    """
    import json
    from graphviz import Digraph
    try:
        import keras as keras
        from keras.models import Sequential
        from keras.layers import Dense, Conv2D, MaxPooling2D, Dropout, Flatten, Activation
    except:
        import tensorflow.keras as keras
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Dropout, Flatten, Activation
    input_layer = 0
    hidden_layers_nr = 0
    layer_types = []
    hidden_layers = []
    output_layer = 0
    for layer in model.layers:
        if layer == model.layers[0]:
            input_layer = int(str(layer.input_shape).split(',')[1][1:-1])
            hidden_layers_nr += 1
            if type(layer) == Dense:
                hidden_layers.append(int(str(layer.output_shape).split(',')[1][1:-1]))
                layer_types.append('Dense')
            else:
                hidden_layers.append(1)
                if type(layer) == Conv2D:
                    layer_types.append('Conv2D')
                elif type(layer) == MaxPooling2D:
                    layer_types.append('MaxPooling2D')
                elif type(layer) == Dropout:
                    layer_types.append('Dropout')
                elif type(layer) == Flatten:
                    layer_types.append('Flatten')
                elif type(layer) == Activation:
                    layer_types.append('Activation')
        else:
            if layer == model.layers[-1]:
                output_layer = int(str(layer.output_shape).split(',')[1][1:-1])
            else:
                hidden_layers_nr += 1
                if type(layer) == Dense:
                    hidden_layers.append(int(str(layer.output_shape).split(',')[1][1:-1]))
                    layer_types.append('Dense')
                else:
                    hidden_layers.append(1)
                    if type(layer) == Conv2D:
                        layer_types.append('Conv2D')
                    elif type(layer) == MaxPooling2D:
                        layer_types.append('MaxPooling2D')
                    elif type(layer) == Dropout:
                        layer_types.append('Dropout')
                    elif type(layer) == Flatten:
                        layer_types.append('Flatten')
                    elif type(layer) == Activation:
                        layer_types.append('Activation')
        last_layer_nodes = input_layer
        nodes_up = input_layer
        if type(model.layers[0]) != Dense:
            last_layer_nodes = 1
            nodes_up = 1
            input_layer = 1

        graph = Digraph('Graph', filename=filename)
        n = 0
        graph.graph_attr.update(splines='false', nodesep='1', ranksep='2')
        # Input Layer
        with graph.subgraph(name='cluster_input') as c:

            if type(model.layers[0]) == Dense:
                input_units = int(str(model.layers[0].input_shape).split(',')[1][1:-1])
                the_label = f'Input Units: {input_units}'
                if input_units > 10:
                    the_label += f' (+{str(input_units - 10)} more)'
                    input_layer = 10
                the_label += f'\nActivation: {str(model.layers[0].get_config()["activation"])}'
                c.attr(color='white')
                for i in range(0, input_layer):
                    n += 1
                    c.node(str(n))
                    c.attr(rank='same')
                    c.node_attr.update(color='#2ecc71', style='filled', fontcolor='#2ecc71', shape='circle')
                c.node(str(n+1)*3, the_label, shape='rectangle', fontsize='18', color='white', fontcolor='black')

            elif type(model.layers[0]) == Conv2D:
                pxls = str(model.layers[0].input_shape).split(',')
                clr = int(pxls[3][1:-1])
                if clr == 1:
                    clrmap = 'Grayscale'
                    the_color = 'black:white'
                elif clr == 3:
                    clrmap = 'RGB'
                    the_color = '#e74c3c:#3498db'
                else:
                    clrmap = ''
                n += 1
                c.node(str(n), label=f'Image\n{pxls[1]} x{pxls[2]} pixels\n{clrmap}', fontcolor='white', shape='square', style='filled', fillcolor=the_color)
            else:
                raise ValueError('Keras Visualizer: Layer not supported for visualizing')

        # Hidden Layers
        for i in range(0, hidden_layers_nr):
            with graph.subgraph(name='cluster_' + str(i + 1)) as c:
                if layer_types[i] == 'Dense':
                    c.attr(color='white')
                    c.attr(rank='same')
                    # If hidden_layers[i] > 10, dont include all
                    units = int(str(model.layers[i].output_shape).split(',')[1][1:-1])
                    the_label = f'Units: {units}'
                    if units > 10:
                        the_label += f' (+{str(units - 10)} more)'
                        hidden_layers[i] = 10
                    the_label += f'\nActivation: {str(model.layers[i].get_config()["activation"])}'
                    c.node(str(n)*3, the_label, shape='rectangle', fontsize='18', color='white', fontcolor='black')
                    for j in range(0, hidden_layers[i]):
                        n += 1
                        c.node(str(n), shape='circle', style='filled', color='#3498db', fontcolor='#3498db')
                        for h in range(nodes_up - last_layer_nodes + 1, nodes_up + 1):
                            graph.edge(str(h), str(n))
                    last_layer_nodes = hidden_layers[i]
                    nodes_up += hidden_layers[i]
                elif layer_types[i] == 'Conv2D':
                    c.attr(style='filled', color='#5faad0')
                    n += 1
                    activation = str(model.layers[0].get_config()["activation"])
                    kernel_size = str(model.layers[i].get_config()['kernel_size']).split(',')[0][1] + 'x' + \
                                  str(model.layers[i].get_config()['kernel_size']).split(',')[1][1: -1]
                    filters = str(model.layers[i].get_config()['filters'])
                    c.node('conv_' + str(n), label=f'Convolutional Layer\nKernel Size: {kernel_size}\nFilters: {filters}\nActivation: {activation}', shape='square')
                    c.node(str(n), label=filters + '\nFeature Maps', shape='square')
                    graph.edge('conv_' + str(n), str(n))
                    for h in range(nodes_up - last_layer_nodes + 1, nodes_up + 1):
                        graph.edge(str(h), 'conv_' + str(n))
                    last_layer_nodes = 1
                    nodes_up += 1
                elif layer_types[i] == 'MaxPooling2D':
                    c.attr(color='white')
                    n += 1

                    pool_size = str(model.layers[i].get_config()['pool_size']).split(',')[0][1] + 'x' + \
                                str(model.layers[i].get_config()['pool_size']).split(',')[1][1: -1]
                    c.node(str(n), label=f'Max Pooling\nPool Size: {pool_size}', style='filled', fillcolor='#8e44ad', fontcolor='white')
                    for h in range(nodes_up - last_layer_nodes + 1, nodes_up + 1):
                        graph.edge(str(h), str(n))
                    last_layer_nodes = 1
                    nodes_up += 1
                elif layer_types[i] == 'Flatten':
                    n += 1
                    c.attr(color='white')
                    c.node(str(n), label='Flattening', shape='invtriangle', style='filled', fillcolor='#2c3e50', fontcolor='white')
                    for h in range(nodes_up - last_layer_nodes + 1, nodes_up + 1):
                        graph.edge(str(h), str(n))
                    last_layer_nodes = 1
                    nodes_up += 1
                elif layer_types[i] == 'Dropout':
                    n += 1
                    c.attr(color='white')
                    c.node(str(n), label='Dropout Layer', style='filled', fontcolor='white', fillcolor='#f39c12')
                    for h in range(nodes_up - last_layer_nodes + 1, nodes_up + 1):
                        graph.edge(str(h), str(n))
                    last_layer_nodes = 1
                    nodes_up += 1
                elif layer_types[i] == 'Activation':
                    n += 1
                    c.attr(color='white')
                    fnc = model.layers[i].get_config()['activation']
                    c.node(str(n), shape='octagon', label=f'Activation Layer\nFunction: {fnc}', style='filled', fontcolor='black',
                           fillcolor='#00b894')
                    for h in range(nodes_up - last_layer_nodes + 1, nodes_up + 1):
                        graph.edge(str(h), str(n))
                    last_layer_nodes = 1
                    nodes_up += 1

        # Output Layer
        with graph.subgraph(name='cluster_output') as c:
            if type(model.layers[-1]) == Dense:
                output_units = int(str(model.layers[-1].output_shape).split(',')[1][1:-1])
                the_label = f'Output Units: {output_units}'
                if output_units > 10:
                    the_label += f' (+{str(output_units - 10)} more)'
                    output_layer = 10
                the_label += f'\nActivation: {str(model.layers[0].get_config()["activation"])}'
                c.node(str(n) * 3, the_label, shape='rectangle', fontsize='18', color='white', fontcolor='black')
                c.attr(color='white')
                c.attr(rank='same')
                c.attr(labeljust='1')
                for i in range(1, output_layer + 1):
                    n += 1
                    c.node(str(n), shape='circle', style='filled', color='#e74c3c', fontcolor='#e74c3c')
                    for h in range(nodes_up - last_layer_nodes + 1, nodes_up + 1):
                        graph.edge(str(h), str(n))
                c.node_attr.update(color='#2ecc71', style='filled', fontcolor='#2ecc71', shape='circle')

        graph.attr(arrowShape='none')
        graph.edge_attr.update(arrowhead='none', color='#707070')

    try:
        if format is not None:
            graph.render(format=format, view=view)
        else:
            graph.save()
    except Exception:
        raise ValueError('Keras Visualizer: Error while visualizing')
