from setuptools import setup, find_packages

# reading long description from file
with open("README.md", encoding="utf-8") as file:
    long_description = file.read()


# specify requirements of your package here
REQUIREMENTS = ["pygame", "black", "pre-commit"]


# calling the setup function
setup(name="snake",
      version="0.1",
      description="A simple snake game",
      long_description=long_description,
      long_description_content_type = "text/markdown",
      url="https://github.com/douglas-cpp/snake",
      author="Douglas",
      author_email="douglasc.dev@gmail.com",
      license="Apache License 2.0",
      packages=find_packages(include=["snake"]),
      install_requires=REQUIREMENTS,
      keywords="game"
      )
