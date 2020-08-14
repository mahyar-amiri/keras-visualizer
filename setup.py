import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="keras-visualizer",
    version="2.4",
    author="Mahyar Amiri",
    description="A Keras Model Visualizer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lordmahyar/keras-visualizer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
