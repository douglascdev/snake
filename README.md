# snake
![alt text](https://github.com/douglas-cpp/snake/blob/master/snake.png)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A snake game made with Pygame and Python3, still missing some features.

## Contribute
You can contribute by solving any of our open issues, or  any other improvement you feel like doing!
- Fork the repository and clone your fork using git
- Create a new branch for your changes
- Install the dev requirements with `pip3 install -r dev-requirements.txt`
- Run `pre-commit install`. After every commit, pre-commit will use black to format the style of your code, keeping a consistent style for the whole project. If your files get reformatted, your changes(and black's) will stay staged and you'll have to commit again. You can also run `black .` to reformat the files, or `black . --check` to see if there is anything that needs to be reformated.
- Code and test your functionality 
- Create a pull request

## Install
- Install python3 from https://www.python.org/download/releases/3.0/
- Install the game with `pip install git+https://github.com/douglas-cpp/snake`
- Run it with `python -c "from snake import main;main.main()"`
