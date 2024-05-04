# StudyBud Web Application

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed the latest version of Python.
- You have installed Git (if you plan to clone the repository).

## Installation

### Setting up the Virtual Environment

1. **Windows:**

   Open Command Prompt and navigate to your project directory. Then, run the following commands:

          python -m venv venv .\venv\Scripts\activate

2. **macOS/Linux:**

   Open Terminal, navigate to your project directory, and run the following commands:

          python3 -m venv venv source venv/bin/activate


### Installing Dependencies

After setting up the virtual environment and activating it, you need to install the required dependencies. Navigate to your project directory and run:

          pip install -r requirements.txt


This command installs all the dependencies listed in your `requirements.txt` file. Ensure that you have a `requirements.txt` file in your project directory with all the necessary packages listed.

## Running the Application

To run the application, use the following command:

          python manage.py runserver


This command starts the Django development server. By default, the server runs on `http://127.0.0.1:8000/`. You can access your application by opening this URL in your web browser.

