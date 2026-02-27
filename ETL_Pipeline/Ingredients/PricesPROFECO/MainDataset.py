import pandas as pd

from .DownloadRawDataset import MainDownload
from .CleanDataset import MainClean
from .TransformDataset import MainTransform

def MainDatasetETL():
    DatasetPath_1 , DatasetPath_2 = MainDownload()

    CompleteDataset = pd.concat([MainClean(DatasetPath_1,1),MainClean(DatasetPath_2,2)])
    CompleteDataset.to_csv(DatasetPath_1.parent/'dataset.csv',index=False)

    CleanDataset = MainTransform(CompleteDataset)
    CleanDataset.to_csv(DatasetPath_1.parent/'clean.csv',index=False)

    return DatasetPath_1.parent/'clean.csv'