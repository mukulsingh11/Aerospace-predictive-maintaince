from collections import namedtuple

DataIngestionConfig = namedtuple('DataIngestionConfig',['dataset_download_url','ingested_dir','ingested_train_dir',
                                                        'ingested_test_dir'])

DataValidationConfig = namedtuple('DataValidationConfig',['schema_file_path'])
















TrainingPipelineConfig = namedtuple('TrainingPipelineConfig',['artifact_dir'])        
                                              

