# CSV to JSON Endpoint Tool

A simple Python tool to upload a CSV file and convert it into a JSON endpoint. This tool allows you to query and filter results via GET requests, making it easy to access your data for local endpoint testing.

## Features

- Upload a CSV file to create a JSON endpoint
- Query and filter results using GET requests
- Mock endpoints for local development
- Data validation and testing
- API design and prototyping

## Requirements

- Python 3.x
- Flask==3.0.3
- Werkzeug==3.0.2

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/KarrDynamics/csv-to-json-endpoint.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd csv-to-json-endpoint
    ```

3. **Create a Python virtual environment:**

    ```bash
    python -m venv venv
    ```

4. **Activate the virtual environment:**

    - **On Windows:**

        ```bash
        venv\Scripts\activate
        ```

    - **On macOS and Linux:**

        ```bash
        source venv/bin/activate
        ```

5. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Run the Flask application:**

    ```bash
    python run.py
    ```

2. **Open your web browser and go to** `http://127.0.0.1:5000`

3. **Upload a CSV file and follow the on-screen instructions to use the tool.**

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
