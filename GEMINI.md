# Project Overview

This is a simple expense tracker web application built with Python and the Flask framework. It uses SQLAlchemy for the ORM and a SQLite database to store expense data. The frontend is built with Bootstrap and includes some JavaScript for interactive charts.

## Key Technologies

*   **Backend:** Python, Flask, Flask-SQLAlchemy
*   **Database:** SQLite
*   **Frontend:** HTML, CSS, JavaScript, Bootstrap, Chart.js
*   **Testing:** Pytest

# Building and Running

## Prerequisites

*   Python 3.x
*   pip

## Installation

1.  Clone the repository.
2.  Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1.  Initialize the database (this only needs to be done once):

    The application automatically creates the database file (`expenses.db`) in the project root if it doesn't exist when the application starts.

2.  Run the Flask development server:

    ```bash
    python app.py
    ```

3.  Open your browser and navigate to `http://127.0.0.1:5000`.

## Running Tests

To run the automated tests, use `pytest`:

```bash
pytest
```

# Development Conventions

*   **Code Style:** The Python code generally follows the PEP 8 style guide.
*   **Testing:** Tests are located in `test_app.py` and use the `pytest` framework. The tests use an in-memory SQLite database for isolation.
*   **Database:** The application uses a SQLite database (`expenses.db`) for storing data. The database schema is defined in `app.py` using SQLAlchemy.
*   **Templates:** The HTML templates are located in the `templates` directory and use the Jinja2 templating engine.
