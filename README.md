# Python Environment Hub

Python Environment Hub is a powerful and user-friendly tool designed to help developers manage their Python virtual environments and development tools efficiently. With this application, you can easily create, activate, and delete Python environments, open Jupyter Notebooks and Spyder IDE, and add custom software launchers.

## Features
- **Create Python Environments**: Easily create new virtual environments with your chosen version of Python.
- **Activate Environments**: Select and activate environments from a list of available environments.
- **Delete Environments**: Safely delete virtual environments after confirmation.
- **Open Jupyter Notebook**: Launch Jupyter Notebook within the activated environment.
- **Open Spyder**: Start the Spyder IDE within the activated environment.
- **Add Custom Software**: Add custom software launchers to the hub.
- **Remove Custom Software**: Remove previously added custom software launchers.
- **Help Section**: Access help information and useful links for downloading and installing various development tools.

## Installation
1. **Clone the Repository**:
    ```sh
    git clone https://github.com/yourusername/python-environment-hub.git
    cd python-environment-hub
    ```
2. **Install Required Libraries**:
    ```sh
    pip install -r requirements.txt
    ```

## Usage
1. **Run the Application**:
    ```sh
    python luncher_env_python.py
    ```
2. **Main Interface**:
    - **Environment Manager**: Create, activate, and delete Python virtual environments.
    - **Tools**: Open Jupyter Notebook, Spyder IDE, and access the help section.
    - **Custom Software**: Add and remove custom software launchers.

## Help Section
- To open a Jupyter Notebook in your active environment, type the following command:
    ```sh
    jupyter notebook
    ```
- To download Jupyter and install, go to the following link:
    [Jupyter Installation](https://jupyter.org/install)
- To download Spyder, go to the following link:
    [Spyder IDE](https://www.spyder-ide.org/)
- To download Notepad++, go to the following link:
    [Notepad++](https://notepad-plus-plus.org/downloads/)
- To download PyCharm Community Edition, go to the following link:
    [PyCharm Community Edition](https://www.jetbrains.com/pycharm/download/)

- To activate an environment manually, type the following command + environment name:
    ```sh
    source /path_to_env/bin/activate (Linux/Mac)
    .\path_to_env\Scripts\activate (Windows)
    ```
- To create an environment manually, type the following command:
    ```sh
    python -m venv env_name
    ```
- To install Python libraries, use pip. To know more, refer to the following link:
    [pip Installation](https://pip.pypa.io/en/stable/installation/)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing
Contributions are welcome! Please read the [CONTRIBUTING](CONTRIBUTING.md) guidelines first.

## Acknowledgements
- Inspired by the need for an efficient Python environment management tool.
- Icons and design elements are credited to their respective creators.

## Contact
If you have any questions, feel free to open an issue or reach out to the maintainers.
