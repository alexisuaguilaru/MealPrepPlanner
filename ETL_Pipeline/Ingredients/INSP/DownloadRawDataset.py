from ...Utils import DownloadDataset

def MainDownload():
    URLPath = 'https://insp.mx/resources/images/stories/2022/docs/220615_bam_1811.xlsx'
    DatasetPath = './Datasets/IngredientsNutritional/INSP/raw.xlsx'
    
    dataset_path = DownloadDataset(
        URLPath,
        'https://insp.mx/informacion-relevante/bam-bienvenida',
        DatasetPath,
    )
    return dataset_path