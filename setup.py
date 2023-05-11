from setuptools import setup, find_packages

setup(
    name="barcode-scanner",
    version="0.0.1",
    packages=find_packages(),
    author="Dmitry Kalinin",
    author_email="kalinin.mitko@gmail.com",
    install_requires=[
        "pyusb",
    ],
    url="https://github.com/null-none/barcode-scanner",
)
