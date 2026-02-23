from ...Utils import DownloadDataset

def MainDownload():
    DatasetPath = './Datasets/IngredientsPrices/PROFECO/raw.csv'
    dataset_path = DownloadDataset(
        'https://repodatos.atdt.gob.mx/api_update/profeco/programa_quien_es_quien_precios_2025/11-2025_01.csv',
        'https://www.datos.gob.mx/dataset/',
        DatasetPath,
    )

    return dataset_path