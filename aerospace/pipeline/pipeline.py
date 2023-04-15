import os ,sys
from aerospace.logger import logging
from aerospace.exception import CustomException
from aerospace.constant import *
from aerospace.entity.config_entity import *
from aerospace.utils import read_yaml_file
from aerospace.components.data_ingestion import DataIngestion
from aerospace.components.data_validation import DataValidation
from aerospace.entity.artifact_entity import DataIngestionArtifact
from aerospace.components.data_validation import DataValidationArtifact
from aerospace.config.configuration import Configuration 


class Pipeline():
    def __init__(self, config:Configuration = Configuration()) ->None:
        try:
            self.config=config
        except Exception as e:
            raise CustomException(e,sys) from e

    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            data_ingestion = DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())
            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise CustomException(e,sys) from e



    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact)->DataIngestionArtifact:
        try:
            data_validation=DataValidation(data_validation_config=self.config.get_data_validation_config(),
                                            data_ingestion_artifact=DataIngestionArtifact)
            return data_validation.initiate_data_validation
        except Exception as e:
            raise CustomException(e,sys) from e


   
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
        except Exception as e:
            raise CustomException(e,sys) from e

            