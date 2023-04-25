import os , sys
from aerospace.logger import logging
from aerospace.exception import CustomException
from aerospace.constant import *
from aerospace.entity.config_entity import DataIngestionConfig
from aerospace.entity.artifact_entity import DataIngestionArtifact
from aerospace.utils.utils import read_yaml_file
from aerospace.config.configuration import Configuration
import pandas as pd
import numpy as np
from six.moves import urllib
from datetime import date
from sklearn.model_selection import train_test_split


class DataIngestion:

    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            logging.info("*********************** Data Ingestion is started *******************")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CustomException(e,sys) from e
        

    def download_data(self)->str:

        try:
            download_url = self.data_ingestion_config.dataset_download_url

            raw_data_dir = self.data_ingestion_config.raw_data_dir

            os.makedirs(raw_data_dir,exist_ok=True)

            aerospace_file_name = os.path.basename(download_url)

            raw_file_path = os.path.join(raw_data_dir,aerospace_file_name)
            logging.info(f"Downloading file from :[{download_url}] into :[{raw_file_path}]")

            urllib.request.urlretrieve(download_url,raw_file_path)

            logging.info(f"[{raw_file_path}] has been downloaded successfully")
            return raw_file_path


        except Exception as e:
            raise CustomException(e,sys) from e
        
    def split_data_as_train_test(self)->DataIngestionArtifact:
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            file_name = os.listdir(raw_data_dir)[0]

            aerospace_file_path = os.path.join(raw_data_dir,file_name)

            logging.info(f"Reading csv file: [{aerospace_file_path}]")

            todays_data = date.today()
            current_year = todays_data.year

            aerospace_dataframe = pd.read_csv(aerospace_file_path)

            aerospace_dataframe.drop([COLUMN_ID,COLUMN_PRODUCT_ID], axis = 1 , inplace=True)
            aerospace_dataframe[COLUMN_Failure_Type] = np.where(aerospace_dataframe[COLUMN_Failure_Type] == 'Denied', 1,0)

            logging.info(f"splitting data into train and test")

            train_set=None
            test_set=None 

            train_set , test_set = train_test_split(aerospace_dataframe,test_size=0.25 , random_state=40)

            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir,file_name)

            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir,file_name)

            if train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir,exist_ok=True)
                logging.info(f"Expoorting training dataset to file: [{train_file_path}]")
                train_set.to_csv(train_file_path,index=False)

            if test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir,exist_ok=True)
                logging.info(f" Exporting test dataset to file: [{test_file_path}]")
                test_set.to_csv(test_file_path , index =False)

            data_ingestion_artifact = DataIngestionArtifact(train_file_path=train_file_path,
                                                            test_file_path=test_file_path,
                                                            is_ingested=True,
                                                            message = f"Data Ingestion artifact:[{data_ingestion_artifact}]")
        except Exception as e:
            raise CustomException(e,sys) from e
        
    def initiate_data_ingestion(self):
        try:
            raw_file_path = self.download_data()
            return self.split_data_as_train_test()
        except Exception as e:
            raise CustomException(e, sys)from e



