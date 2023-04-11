def visualizer(model, file_name='graph', file_format=None, view=False, settings=None):
    """Visualize a Sequential model.

    # Arguments

        model: a Keras model instance.

        file_name: where to save the visualization.

        file_format: file format to save 'pdf', 'png'.

        view: open file after process if True.

        settings: dictionary of valid configurations.

    * change format to 'png' or 'pdf' to save visualization file
    """
    from graphviz import Digraph

    main_settings = {
        # ALL LAYERS
        'MAX_NEURONS': 10,
        'ARROW_COLOR': '#707070',
        # INPUT LAYERS
        'INPUT_DENSE_COLOR': '#2ecc71',
        'INPUT_EMBEDDING_COLOR': 'black',
        'INPUT_EMBEDDING_FONT': 'white',
        'INPUT_GRAYSCALE_COLOR': 'black:white',
        'INPUT_GRAYSCALE_FONT': 'white',
        'INPUT_RGB_COLOR': '#e74c3c:#3498db',
        'INPUT_RGB_FONT': 'white',
        'INPUT_LAYER_COLOR': 'black',
        'INPUT_LAYER_FONT': 'white',
        # HIDDEN LAYERS
        'HIDDEN_DENSE_COLOR': '#3498db',
        'HIDDEN_CONV_COLOR': '#5faad0',
        'HIDDEN_CONV_FONT': 'black',
        'HIDDEN_POOLING_COLOR': '#8e44ad',
        'HIDDEN_POOLING_FONT': 'white',
        'HIDDEN_FLATTEN_COLOR': '#2c3e50',
        'HIDDEN_FLATTEN_FONT': 'white',
        'HIDDEN_DROPOUT_COLOR': '#f39c12',
        'HIDDEN_DROPOUT_FONT': 'black',
        'HIDDEN_ACTIVATION_COLOR': '#00b894',
        'HIDDEN_ACTIVATION_FONT': 'black',
        'HIDDEN_LAYER_COLOR': 'black',
        'HIDDEN_LAYER_FONT': 'white',
        # OUTPUT LAYER
        'OUTPUT_DENSE_COLOR': '#e74c3c',
        'OUTPUT_LAYER_COLOR': 'black',
        'OUTPUT_LAYER_FONT': 'white',
    }

    settings = {**main_settings, **settings} if settings is not None else {**main_settings}
    max_neurons = settings['MAX_NEURONS']

    input_layer = 0
    hidden_layers_nr = 0
    layer_types = []
    hidden_layers = []
    output_layer = 0

    for num, layer in enumerate(model.layers, 1):
        if num == 1:
            input_layer = layer.input_shape[1] if type(layer.input_shape) == tuple else layer.input_shape[0][1]
        if num == len(model.layers):
            output_layer = layer.output_shape[1]
        else:
            hidden_layers_nr += 1
            hidden_layers.append(layer.output_shape[1] if layer.__class__.__name__ == 'Dense' else 1)
            layer_types.append(f'{layer.__class__.__name__}')

        last_layer_nodes = input_layer
        nodes_up = input_layer

        if model.layers[0].__class__.__name__ != 'Dense':
            last_layer_nodes = 1
            nodes_up = 1
            input_layer = 1

        # VISUALIZE MODEL
        graph = Digraph('Graph', filename=file_name)
        n = 0
        graph.graph_attr.update(
            nodesep='1',  # X-SPACE
            ranksep='2',  # Y-SPACE
            splines='false'
        )

        # Input Layer
        with graph.subgraph(name='cluster_input') as c:
            # DENSE LAYER INPUT
            layer = model.layers[0]
            if layer.__class__.__name__ == 'Dense':
                input_units = layer.input_shape[1]
                label_dense_input = f'Input Units: {input_units}'
                if max_neurons is not None and input_units > max_neurons:
                    label_dense_input += f' (+{input_units - max_neurons} more)'
                    input_layer = max_neurons
                label_dense_input += f'\nActivation: {layer.get_config()["activation"]}'
                c.attr(color='white')
                for i in range(0, input_layer):
                    n += 1
                    c.node(str(n))
                    c.attr(rank='same')
                    c.node_attr.update(shape='circle', style='filled', color=settings['INPUT_DENSE_COLOR'], fontcolor=settings['INPUT_DENSE_COLOR'])
                c.node(str(n + 1) * 3, label_dense_input, shape='rectangle', fontsize='18', color='white', fontcolor='black')
            # EMBEDDING LAYER INPUT
            elif layer.__class__.__name__ == 'Embedding':
                input_dim = layer.input_dim
                output_dim = layer.output_dim
                n += 1
                c.node(str(n), label=f'Embedding\nInput Dim: {input_dim}\nOutput Dim: {output_dim}', shape='square', style='filled', fillcolor=settings['INPUT_EMBEDDING_COLOR'], fontcolor=settings['INPUT_EMBEDDING_FONT'])
            # CONV2D LAYER INPUT (IMAGE)
            elif 'Conv' in layer.__class__.__name__:
                pxls = layer.input_shape
                clr = pxls[-1]
                node_color = 'white'
                node_font = 'black'
                if clr == 1:
                    clrmap = 'Grayscale'
                    node_color = settings['INPUT_GRAYSCALE_COLOR']
                    node_font = settings['INPUT_GRAYSCALE_FONT']
                elif clr == 3:
                    clrmap = 'RGB'
                    node_color = settings['INPUT_RGB_COLOR']
                    node_font = settings['INPUT_RGB_FONT']
                else:
                    clrmap = ''
                n += 1
                c.node(str(n), label=f'Image\n{pxls[-3]} x {pxls[-2]} pixels\n{clrmap}', shape='square', style='filled', fillcolor=node_color, fontcolor=node_font)
            else:
                # raise ValueError('[Keras Visualizer] Input Layer is not supported for visualizing')
                c.attr(color='white')
                n += 1
                input_layer = layer.input_shape[1] if type(layer.input_shape) == tuple else layer.input_shape[0][1]
                label_layer = f'{layer.__class__.__name__}\nshape= {input_layer}'
                c.node(str(n), label=label_layer, shape='egg', style='filled', fillcolor=settings['INPUT_LAYER_COLOR'], fontcolor=settings['INPUT_LAYER_FONT'])

        # Hidden Layers
        for i in range(0, hidden_layers_nr):
            with graph.subgraph(name='cluster_' + str(i + 1)) as c:
                # Dense Layer
                if layer_types[i] == 'Dense':
                    c.attr(color='white')
                    c.attr(rank='same')
                    # If hidden_layers[i] > MAX_NEURONS, dont include all
                    units = model.layers[i].output_shape[1]
                    label_dense = f'Units: {units}'
                    if max_neurons is not None and units > max_neurons:
                        label_dense += f' (+{units - max_neurons} more)'
                        hidden_layers[i] = max_neurons
                    label_dense += f'\nActivation: {model.layers[i].get_config()["activation"]}'
                    c.node(str(n) * 3, label_dense, shape='rectangle', fontsize='18', color='white', fontcolor='black')
                    for j in range(0, hidden_layers[i]):
                        n += 1
                        c.node(str(n), shape='circle', style='filled', color=settings['HIDDEN_DENSE_COLOR'], fontcolor=settings['HIDDEN_DENSE_COLOR'])
                        for h in range(nodes_up - last_layer_nodes + 1, nodes_up + 1):
                            graph.edge(str(h), str(n))
                    last_layer_nodes = hidden_layers[i]
                    nodes_up += hidden_layers[i]
                # Convolutional Layer
                elif 'Conv' in layer_types[i]:
                    c.attr(style='filled', color=settings['HIDDEN_CONV_COLOR'])
                    n += 1
                    activation = model.layers[0].get_config().get('activation')
                    kernel_size = model.layers[i].get_config().get('kernel_size')
                    filters = model.layers[i].get_config().get('filters', 0)
                    label_conv = f'{layer_types[i]} Layer\nKernel Size: {kernel_size}\nFilters: {filters}\nActivation: {activation}'
                    c.node('conv_' + str(n), label=label_conv, shape='square', fontcolor=settings['HIDDEN_CONV_FONT'])
                    c.node(str(n), label=f'{filters}\nFeature Maps', shape='square', fontcolor=settings['HIDDEN_CONV_FONT'])
                    graph.edge('conv_' + str(n), str(n))
                    for h in range(nodes_up - last_layer_nodes + 1, nodes_up + 1):
                        graph.edge(str(h), 'conv_' + str(n))
                    last_layer_nodes = 1
                    nodes_up += 1
                # Pooling Layer
                elif 'Pooling' in layer_types[i]:
                    c.attr(color='white')
                    n += 1
                    pool_size = model.layers[i].get_config().get('pool_size', None)
                    label_pooling = f'{layer_types[i]}' + (f'\nPool Size: {pool_size}' if pool_size is not None else '')
                    c.node(str(n), label=label_pooling, shape='invtrapezium', style='filled', fillcolor=settings['HIDDEN_POOLING_COLOR'], fontcolor=settings['HIDDEN_POOLING_FONT'])
                    for h in range(nodes_up - last_layer_nodes + 1, nodes_up + 1):
                        graph.edge(str(h), str(n))
                    last_layer_nodes = 1
                    nodes_up += 1
                # Flatten Layer
                elif layer_types[i] == 'Flatten':
                    n += 1
                    c.attr(color='white')
                    c.node(str(n), label='Flattening', shape='triangle', style='filled', fillcolor=settings['HIDDEN_FLATTEN_COLOR'], fontcolor=settings['HIDDEN_FLATTEN_FONT'])
                    for h in range(nodes_up - last_layer_nodes + 1, nodes_up + 1):
                        graph.edge(str(h), str(n))
                    last_layer_nodes = 1
                    nodes_up += 1
                # Dropout Layer
                elif 'Dropout' in layer_types[i]:
                    n += 1
                    c.attr(color='white')
                    rate = model.layers[i].get_config().get('rate', None)
                    label_dropout = f'{layer_types[i]}\nRate: {rate}'
                    c.node(str(n), label=label_dropout, shape='Mcircle', style='filled', fillcolor=settings['HIDDEN_DROPOUT_COLOR'], fontcolor=settings['HIDDEN_DROPOUT_FONT'])
                    for h in range(nodes_up - last_layer_nodes + 1, nodes_up + 1):
                        graph.edge(str(h), str(n))
                    last_layer_nodes = 1
                    nodes_up += 1
                # Activation Layer
                elif layer_types[i] == 'Activation':
                    n += 1
                    c.attr(color='white')
                    fnc = model.layers[i].get_config().get('activation')
                    c.node(str(n), label=f'Activation Layer\nFunction: {fnc}', shape='octagon', style='filled', fillcolor=settings['HIDDEN_ACTIVATION_COLOR'], fontcolor=settings['HIDDEN_ACTIVATION_FONT'])
                    for h in range(nodes_up - last_layer_nodes + 1, nodes_up + 1):
                        graph.edge(str(h), str(n))
                    last_layer_nodes = 1
                    nodes_up += 1
                # OTHER Layers
                else:
                    c.attr(color='white')
                    n += 1
                    label_layer = f'{layer_types[i]} Layer'
                    c.node(str(n), label=label_layer, shape='egg', style='filled', fillcolor=settings['HIDDEN_LAYER_COLOR'], fontcolor=settings['HIDDEN_LAYER_FONT'])
                    for h in range(nodes_up - last_layer_nodes + 1, nodes_up + 1):
                        graph.edge(str(h), str(n))
                    last_layer_nodes = 1
                    nodes_up += 1

        # Output Layer
        with graph.subgraph(name='cluster_output') as c:
            if model.layers[-1].__class__.__name__ == 'Dense':
                output_units = model.layers[-1].output_shape[1]
                label_dense_output = f'Output Units: {output_units}'
                if max_neurons is not None and output_units > max_neurons:
                    label_dense_output += f' (+{output_units - max_neurons} more)'
                    output_layer = max_neurons
                label_dense_output += f'\nActivation: {model.layers[-1].get_config()["activation"]}'
                c.node(str(n) * 3, label_dense_output, shape='rectangle', fontsize='18', color='white', fontcolor='black')
                c.attr(color='white')
                c.attr(rank='same')
                c.attr(labeljust='1')
                for i in range(1, output_layer + 1):
                    n += 1
                    c.node(str(n), shape='circle', style='filled', color=settings['OUTPUT_DENSE_COLOR'], fontcolor=settings['OUTPUT_DENSE_COLOR'])
                    for h in range(nodes_up - last_layer_nodes + 1, nodes_up + 1):
                        graph.edge(str(h), str(n))
                # c.node_attr.update(color='#2ecc71', style='filled', fontcolor='#2ecc71', shape='circle')
            else:
                # raise ValueError('[Keras Visualizer] Output layer is not supported for visualizing')
                c.attr(color='white')
                n += 1
                output_layer = layer.output_shape[1] if type(layer.output_shape) == tuple else layer.output_shape[0][1]
                label_layer = f'{layer.__class__.__name__}\nshape= {output_layer}'
                c.node(str(n), label=label_layer, shape='egg', style='filled', fillcolor=settings['OUTPUT_LAYER_COLOR'], fontcolor=settings['OUTPUT_LAYER_FONT'])

        graph.attr(arrowShape='none')
        graph.edge_attr.update(arrowhead='none', color=settings['ARROW_COLOR'])

    # SAVE GRAPH
    try:
        if file_format is not None:
            graph.render(format=file_format, view=view)
        else:
            graph.save()
    except Exception:
        raise ValueError(f'[Keras Visualizer] Error while visualizing: {Exception}')
