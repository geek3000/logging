from flask import Flask
from logger import jsonLogHandler
from flask.logging import default_handler
import logging

app = Flask(__name__)

logger = logging.getLogger()


if app.debug != True:

  logger.removeHandler(default_handler)
  logger.addHandler(jsonLogHandler)

@app.route('/')
def main():
    return "ok"


if __name__ == '__main__':
  app.run(debug=True)
