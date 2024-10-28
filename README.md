# Docker PyEvents

Get Discord notifications when Docker containers die.

## Requirements

- [Docker SDK](https://docker-py.readthedocs.io/en/stable/index.html)
- [Python-dotenv](https://pypi.org/project/python-dotenv/)

> **Warning**: This guide is only necessary if you **are not** running the project inside a Docker container. If you're using Docker, the virtual environment setup is typically not required as isolation is managed by the container itself.

### Creating a virtual environment (venv) and installing requirements

1. **Create the virtual environment:**

   To create a virtual environment, use the following command in your terminal:

   ```bash
   python3 -m venv venv
   ```

   > This will create a folder named *venv* in your current directory.

2. **Activate the virtual environment:**

    After creating it, activate the virtual environment using the appropriate command for your operating system:

    - Linux/MacOS:

    ``` bash
    source venv/bin/activate
    ```

    - Windows:

    ```bash
    .\venv\Scripts\activate
    ```

3. **Install packages from `requirements.txt`:**

    With the virtual environment activated, install the dependencies listed in the `requirements.txt` file:

    ```bash
    pip install -r requirements.txt
    ```

4. **Deactivate the virtual environment (Optional):**

    When you're done using the virtual environment, you can deactivate it with the command:

    ```bash
    deactivate
    ```
