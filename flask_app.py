import threading
from flask import Flask

app = Flask(__name__)


class FlaskThread(threading.Thread):
    def run(self) -> None:
        app.run(debug=False, host='0.0.0.0')  # ssl_context='adhoc'
