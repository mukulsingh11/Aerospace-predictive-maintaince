from aerospace.pipeline.pipeline import Pipeline
from aerospace.logger import logging
from aerospace.exception import CustomException
from aerospace.config.configuration import Configuration
from aerospace.components.data_ingestion import DataIngestion
import os




def main():
    try:
        pipeline = Pipeline()
        pipeline.run_pipeline()

    except Exception as e:
            logging.error(f"{e}")
            print(e)


if __name__ == "__main__":
     main()