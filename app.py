from flask import Flask, request
from logger import jsonLogHandler
from flask.logging import default_handler
import logging

app = Flask(__name__)



if app.debug != True:

  logging.getLogger().addHandler(jsonLogHandler)

  log = logging.getLogger('werkzeug')
  log.disabled = True
  app.logger.setLevel(logging.INFO)
  app.logger.removeHandler(default_handler)
  app.logger.addHandler(jsonLogHandler)


@app.before_request
def before():
    app.logger.info("request")


@app.route('/')
def main():
    return "ok"


if __name__ == '__main__':
  app.run(debug=True)
