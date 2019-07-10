import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="XRD-Converter",
    version="0.0.1",
    author="Jonathan Obenland",
    author_email="jobenland1@gmail.com",
    description="converts xrd files into readable xlsx",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jobenland/XRD-Converter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Python"
    ],
)