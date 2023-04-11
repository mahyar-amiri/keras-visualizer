import setuptools

VERSION = '3.1.2'

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='keras-visualizer',
    version=VERSION,
    license='MIT',
    author='Mahyar Amiri',
    author_email='mmaahhyyaarr@gmail.com',
    description='A Keras Model Visualizer',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/lordmahyar/keras-visualizer',
    packages=setuptools.find_packages(),
    install_requires=['graphviz'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
