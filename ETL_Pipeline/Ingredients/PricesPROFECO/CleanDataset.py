import pandas as pd

from .DownloadRawDataset import MainDownload

def MainClean(DatasetPath,IndexPart):
    ChunkedDataset = pd.read_csv(DatasetPath,chunksize=1000)
    FilteredDataset  = FilterChunksDataset(ChunkedDataset)

    relevant_categories = ['Basicos', 'Frutas y Legumbres','Pescados y Mariscos','Mercados']
    FilteredDataset.query("catalogo in @relevant_categories",inplace=True)
    CleanedDataset = FilteredDataset[['producto','presentacion','categoria','catalogo','precio']].copy()

    CleanedDataset.to_csv(DatasetPath.parent/f'filtered_{IndexPart}.csv',index=False)
    return CleanedDataset

def FilterChunksDataset(ChunkedDatase) -> pd.DataFrame:
    FilteredChunks = []
    for chunk in ChunkedDatase:
        FilteredChunks.append(chunk.query("estado == 'Michoacan'"))
    return pd.concat(FilteredChunks)