# Marley

Turn based card game built using OOP in python pygame

## Setup

- **Python**: Ensure you have Python installed. If not, you can download it from [here](https://www.python.org/downloads/).
- **pygame**: This game requires pygame version 2.5.0.

After you clone this repo and install the prerequisites you can run `main.py` and try it out.

Or you can try it from the browser on my [Replit](https://replit.com/@xbromsson/marley?v=1).

## Quickstart

```bash
# clone repo
git clone https://github.com/xBromsson/marley.git

# change directory
cd marley/

# install dependencies
python -m pip install -r requirements.txt

# run program
python main.py

# quit program
ctrl + c
```

## Development

### Python virtual environment

```bash
# create virtual environment
python -m venv .venv

# activate virtual environment
source .venv/bin/activate

# install dependencies
python -m pip install -r requirements.txt 
```

### Additional tooling

Additional tooling includes but is not limited to:

#### asdf

* Install [asdf](https://asdf-vm.com/guide/getting-started.html#_2-download-asdf)
* Usage
    ```bash
    # add python plugin
    asdf plugin-add python

    # install stable python
    asdf install python <latest|3.10.12>

    # set stable to system python
    asdf global python latest

    # add poetry asdf plugin
    asdf plugin-add poetry https://github.com/asdf-community/asdf-poetry.git

    # install latest version via asdf
    asdf install poetry <latest|1.5.1>

    # set latest version as default
    asdf global poetry latest
    ```

#### poetry

* Install [poetry](https://python-poetry.org/docs/#installation) if not using `asdf`
* Usage
    ```bash
    # use venv in repo
    poetry config virtualenvs.in-project true

    # install dependencies
    poetry install

    # add new dependency
    poetry add <package>

    # remove dependency
    poetry remove <package>

    # activate virtual environment
    poetry shell

    # run program
    python main.py

    # exit virtual environment
    exit
    ```

#### vscode

* Install [vscode](https://code.visualstudio.com/download)
* Setup [vscode settings](.vscode/launch.json)
  * Handles debug settings for generic python programs as well as others (e.g., django, flask, etc.)

#### ruff

* Installed via `poetry` or `pip`
* Add VSCode plugin for [ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)
  * **Optional**: disable pylance in favor of ruff in [repo settings](.vscode/settings.json)
    ```json
    "python.analysis.ignore": [
      "*"
    ],
    ```
* Usage
    ```bash
    # run tests
    ruff

    # run tests with coverage
    ruff --coverage

    # run tests with coverage and open in browser
    ruff --coverage --open
    ```

#### dependabot

* [Dependabot](https://dependabot.com/) is a GitHub tool that automatically creates pull requests to keep dependencies up to date.

#### editorconfig

Handles formatting of files. [Install the editorconfig plugin](https://editorconfig.org/#download) for your editor of choice.
