import pandas as pd

from .DownloadRawDataset import MainDownload
from .CleanDataset import MainClean

def MainDatasetETL():
    DatasetPath_1 , DatasetPath_2 = MainDownload()
    CompleteDataset = pd.concat([MainClean(DatasetPath_1,1),MainClean(DatasetPath_2,2)])
    CompleteDataset.to_csv(DatasetPath_1.parent/'dataset.csv')