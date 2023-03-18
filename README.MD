
# Diploma filer

This project provides a recipe filler for student diplomas in Yandex Practikum
## Table of Contents

- [Project Name](#project-name)
  - [Table of Contents](#table-of-contents)
  - [Badges](#badges)
  - [Description](#description)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Usage](#usage)
  - [License](#license)

![Python](https://img.shields.io/badge/python-3.9-blue.svg)
![aiohttp](https://img.shields.io/badge/aiohttp-3.8.4-blue.svg)

## Description

This project is a Python script for generating fake recipes and posting them to a remote API. The script uses the asyncio library to make asynchronous requests to the API, and also generates fake user data using the Faker library.
## Installation

1. Clone the repository to your local machine:
    ```shell
    https://github.com/vitaliy-chernyshov/diploma_filller.git
    ```
2. Navigate to the project directory:
    ```shell
    cd diploma_filller
    ```
   #### Using Poetry:
3. ```shell
    poetry install
    ```
   #### Using pip:
3. ```shell
    pip install -r requirements.txt
    ```
   
## Configuration
This project can be configured using the constants.py file, located in the root directory of the project. Here are the variables that can be configured:

* `IMAGES_DIR` This variable specifies the path to the directory where images will be saved. By default, the IMAGES_DIR is set to 'images' and located in the base directory of the project. If you want to change the path, simply modify this variable accordingly:
    ```python
    IMAGES_DIR = BASE_DIR / 'path/to/images'
    ```
* `SERVER` This variable specifies the URL for the server that the project will connect to. By default, the SERVER variable is set to `http://localhost:8000`, which means that the project will connect to a server running on the same machine. If you want to connect to a different server, modify this variable accordingly:
    ```python 
    SERVER = 'http://192.168.1.100:8000'
    ```
* `API_URL` This variable specifies the URL for the API endpoint that the project will use to interact with the server. By default, the `API_URL` variable is set to the `SERVER URL` with the `/api/` suffix:
    ```python
    API_URL = urljoin(SERVER, 'api/')
    ```
* `RECIPES_NUMBER` This variable specifies the number of recipes that are generated when the program is run. By default, the `RECIPES_NUMBER` variable is set to `50`. If you want to generate more or fewer recipes, modify this variable accordingly:
    ```python
    RECIPES_NUMBER = 100
    ```
## Usage

Start the script by running the following command in the terminal:
```shell
python main.py
```

## License

MIT