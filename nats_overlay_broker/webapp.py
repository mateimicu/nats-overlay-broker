"""Main Web Entry Ponint."""
from flask import Flask

BROKER = Flask(__name__)

@BROKER.route("/")
def healtcheck():
    """Retun the health of the application."""
    return "OK"

if __name__ == "__main__":
    BROKER.run('0.0.0.0')
