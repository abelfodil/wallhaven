# Wallhaven
A Python 3 wrapper around the Wallhaven API.

## Development
This project is being rewritten from scratch. Changes will be added to [CHANGELOG.md](CHANGELOG.md).  
You may expect breaking changes to happen at any time without warnings.

## Contributing
**This section will explain how you can contribute to `wallhaven`.**  

This project uses [poetry](https://python-poetry.org/) for dependency management and packaging.  
1. To get started, follow the [instructions](https://python-poetry.org/docs/) and install `Poetry` on your system.
2. Fork your own copy of the repository.
3. Clone your fork and cd into it.
    ```sh
    git clone https://github.com/<your_username>/wallhaven
    cd wallhaven/
    ```
4. Using `poetry`, activate a virtual environment and install the dependencies.
    ```sh
    # Create virtual environment
    poetry env use python3

    # Activate it.
    poetry shell

    # Install wallhaven and its dependencies (including dev dependencies).      
    poetry install
    ```
5. Create a branch for your feature and start coding.
   ```
    git checkout -b <my_new_branch>
   ```
6. Finally, all that's left is to commit your changes and create a pull request.
