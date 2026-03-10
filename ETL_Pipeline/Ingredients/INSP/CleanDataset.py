import pandas as pd

def MainClean(DatasetPath):
    Dataset = pd.read_excel(DatasetPath,skiprows=12,skipfooter=3)

    CleanedDataset = Dataset.fillna(0).iloc[:,1:]
    CleanedDataset.to_csv(DatasetPath.parent/f'clean.csv',index=False)

    return CleanedDataset