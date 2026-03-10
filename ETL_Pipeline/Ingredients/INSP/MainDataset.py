import pandas as pd

from .DownloadRawDataset import MainDownload
from .CleanDataset import MainClean

def MainDatasetETL():
    DatasetPath = MainDownload()
    
    MainClean(DatasetPath)

    return DatasetPath.parent/'clean.csv'