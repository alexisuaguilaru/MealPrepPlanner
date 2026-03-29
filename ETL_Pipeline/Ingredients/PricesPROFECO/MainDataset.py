import pandas as pd

from .DownloadRawDataset import MainDownload
from .CleanDataset import MainClean
from .TransformDataset import MainTransform

from ...Utils import DumpMetadata

def MainDatasetETL():
    DatasetPath_1 , DatasetPath_2 = MainDownload()

    CompleteDataset = pd.concat([MainClean(DatasetPath_1,1),MainClean(DatasetPath_2,2)])
    CompleteDataset.to_csv(DatasetPath_1.parent/'dataset.csv',index=False)

    CleanDataset = MainTransform(CompleteDataset)
    CleanDataset.to_csv(DatasetPath_1.parent/'clean.csv',index=True)

    Metadata_PROFECO = [
        {
            'File Name': 'raw_1.csv',
            'Source': 'https://repodatos.atdt.gob.mx/api_update/profeco/programa_quien_es_quien_precios_2025/11-2025_01.csv',
            'Last Update': '2025/12/24',
        },
        {
            'File Name': 'raw_2.csv',
            'Source': 'https://repodatos.atdt.gob.mx/api_update/profeco/programa_quien_es_quien_precios_2025/11-2025_02.csv',
            'Last Update': '2025/12/24',
        },
    ]
    DumpMetadata(Metadata_PROFECO,DatasetPath_1.parent/'metadata.json')

    return DatasetPath_1.parent/'clean.csv'