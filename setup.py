import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nb2di",
    version='0.0.1',
    author="Gokulraj Ramdass",
    author_email="gokulraj.ramdass@sap.com",
    description="Notebook to DI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/grbusiness18/dinb",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)