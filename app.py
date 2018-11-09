from flask import Flask
import logging
import os.path

# make logger
log = logging.getLogger(os.path.basename(__file__))       # create logger
log.setLevel(logging.DEBUG)
# create file handler
ch = logging.StreamHandler()            # log to console
# log debug messages
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handler
formatter = logging.Formatter('[%(asctime)s] - %(name)s - %(levelname)s: %(message)s')
ch.setFormatter(formatter)
# add the handlers to the logger
log.addHandler(ch)


app = Flask(__name__)
app.testing = True
app.env = "development"


@app.route('/')
def hello_world():
    # log.debug("inside hello_world")
    return 'Hello, World!'


app.run(debug=True)
