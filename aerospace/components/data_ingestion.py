import os , sys
from aerospace.logger import logging
from aerospace.exception import CustomException
from aerospace.constant import *
from aerospace.entity.config_entity import DataIngestionConfig
from aerospace.entity.artifact_entity import DataIngestionArtifact
from aerospace.utils import read_yaml_file
from aerospace.config.configuration import Configuration
from datetime import datetime
import pandas as pd
from sklearn.model_selection import train_test_split


class DataIngestion:

    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            logging.info("*********************** Data Ingestion is started *******************")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CustomException(e,sys) from entity




    def download_data(self)->str:
        try:
            download_url = self.data_ingestion_config.dataset_download_url
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            os.makedirs(raw_data_dir,exist_ok=True)
            
            # dataset conection
            predictive_maintaince_file_name = os.path.basename(download_url)
            raw_file_path = os.path.join(raw_data_dir,predictive_maintaince_file_name)

            logging.info(f"Downloading file from :[{download_url}] into :[{raw_file_path}]")
            urllib.request.urlretrive(download_url , raw_file_path)
            logging.info(f"file: [{raw_file_path}] has been download successfully")

            return raw_file_path

        except Exception as e:
            raise CustomException(e,sys) from e


    def split_data_as_train_test(self)-> DataIngestionArtifact:
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            file_name = os.listdir(raw_data_dir)[0]
            
            predictive_maintaince_file_name = os.path.join(raw_data_dir,file_name)
            today_data = data.today()
            current_year = today_current.year
            
            # drop the column
            predictive_maintaince_dataframe = pd.read_csv(predictive_maintaince_file_name)
            predictive_maintaince_dataframe.drop([COLUMN], axis=1 , inplace=True)

            train_set = None 
            test_set = None

            train_set,test_set = train_test_split(predictive_maintaince_dataframe,test_size=0.25 , random_state=35)

            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir,
                                                    file_name)

            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir,
                                                    file_name)

            if train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir,exist_ok=True)
                train_set.to_csv(train_file_path,index=False)

            if test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir,exist_ok=True)
                test_set.to_csv(test_file_path,index=False)

            data_ingestion_artifact = DataIngestionArtifact(train_file_path=train_file_path,
                                                            test_file_path=test_file_path,
                                                            is_ingested = True,
                                                            message = f"data ingestion is completed")
                                                            
        except Exception as e:
            raise CustomException(e,sys) from e


    def initiate_data_ingestion(self):
        try:
            raw_file_path = self.download_data()
            return self.split_data_as_train_test()
        except Exception as e:
            raise CustomException(e,sys) from e