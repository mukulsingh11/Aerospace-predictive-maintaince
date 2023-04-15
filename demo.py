from aerospace.entity.config_entity import DataIngestionConfig
from aerospace.entity.artifact_entity import DataIngestionArtifact
from aerospace.config.configuration import Configuration
import os ,sys
from aerospace.logger import logging
from aerospace.pipeline.pipeline import Pipeline
from aerospace.exception import CustomException

def main():
    try:
        pipeline = Pipeline()
        pipeline.run_pipeline()
    except Exception as e:
            logging.error(f"{e}")
            print(e)


if __name__ == "__main__":
    main()
