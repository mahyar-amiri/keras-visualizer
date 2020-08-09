import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="keras_visualizer",
    version="2.1",
    author="Mahyar Amiri",
    description="A Keras Model Visualizer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lordmahyar/keras_visualizer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)