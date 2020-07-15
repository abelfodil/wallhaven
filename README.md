# Wallhaven
A Python 3 wrapper around the Wallhaven API.

## Development
This project is being rewritten from scratch. Changes will be added to [CHANGELOG.md](CHANGELOG.md).  
You may expect breaking changes to happen at any time without warnings.

## Contributing
**This section will explain how you can contribute to `wallhaven`.**  

This project uses [poetry](https://python-poetry.org/) for dependency management and packaging.  
1. To get started, follow the [instructions](https://python-poetry.org/docs/) and install `Poetry` on your system.
2. Then, clone the repository and cd into it.
    ```sh
    git clone https://github.com/lucasshiva/wallhaven
    cd wallhaven/
    ```
3. Now, using `poetry`, activate a virtual environment.
    ```sh
    # Create virtual environment
    poetry env use python3

    # Activate it.
    poetry shell

    # Install wallhaven and its dependencies.      
    poetry install
    ```
4. After all that, create a branch and start coding.
   ```
    git checkout -b <my_new_branch>
   ```
5. Finally, all that's left is to commit your changes and create a pull request.
