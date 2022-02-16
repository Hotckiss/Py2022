import setuptools

setuptools.setup(
    name="hotckissast",
    version="1.0.1",
    author="hotckiss",
    description="py ast visualizer",
    url="https://github.com/hotckiss/Py2022",
    packages=["hotckissast"],
    python_requires=">=3.9",
    install_requires=["networkx==2.6.3", "pydot==1.4.2"],
)