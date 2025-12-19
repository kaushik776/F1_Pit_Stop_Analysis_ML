from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def home():
    """Renders the homepage of the PIT STOP application.

    Returns:
        str: The rendered HTML content of 'home.html'.
    """
    return render_template('home.html')