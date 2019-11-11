import setuptools


def get_version():
    with open('version.txt') as ver_file:
        version_str = ver_file.readline().rstrip()
    return version_str


setuptools.setup(
    name="nb2di",
    version=get_version(),
    author="Gokulraj Ramdass",
    author_email="gokulraj.ramdass@sap.com",
    description="Notebook to DI",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/grbusiness18/nb2di",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)