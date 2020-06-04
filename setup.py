from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="flixr",
    version="0.0.1",
    description="A command line utility for television show information.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kelvindecosta/flixr",
    author="Kelvin DeCosta",
    author_email="decostakelvin@gmail.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=["sty",],
    entry_points={"console_scripts": ["flixr = flixr.__main__:main",]},
)
