import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="test-lspy",
    version="0.0.9",
    author="Daan Thijs",
    author_email="daan.thijs@hotmail.com",
    description="A localsearch library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nobody1570/lspy",
    packages=setuptools.find_packages(),
    install_requires=[
        'matplotlib>=3.0.2',
        'numpy>=1.15.4',
    ],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
)
