from aerospace.exception import CustomException
from aerospace.logger import logging
import os ,sys
from flask import Flask

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    try:
        raise Exception('We are testing the Custom Exception')
    except Exception as e:
        aerospace = CustomException(e,sys)
        logging.info(aerospace.error_message)
        logging.info("we are testing the logging file")

if __name__ == "__main__":
    app.run(debug=True)



