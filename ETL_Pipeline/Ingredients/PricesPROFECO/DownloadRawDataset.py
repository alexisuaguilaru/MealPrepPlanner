from ...Utils import DownloadDataset

def MainDownload():
    URLPath = 'https://repodatos.atdt.gob.mx/api_update/profeco/programa_quien_es_quien_precios_2025/11-2025_0{}.csv'
    DatasetPath = './Datasets/IngredientsPrices/PROFECO/raw_{}.csv'
    
    for index_part in range(1,3):
        dataset_path = DownloadDataset(
            URLPath.format(index_part),
            'https://www.datos.gob.mx/dataset/',
            DatasetPath.format(index_part),
        )
        yield dataset_path