from pathlib import Path

from ...Utils import DownloadPDF , DumpMetadata

def MainDownloading():
    BasePath = './Datasets/Documents/SEP'
    base_path = Path(BasePath)
    base_path.mkdir(parents=True,exist_ok=True)

    ListMetadata = []

    LinkFiles = [
        'https://educacionbasica.sep.gob.mx/multimedia/RSC/BASICA/Documento/201611/201611-3-RSC-l100yBJI2X-alimentacion_saludable.pdf',
        'https://laescuelaesnuestra.sep.gob.mx/storage/recursos/2026/01/vB5jTYJmq1-20251217_EB_GUIA_ALIMENTACION_V2.pdf',
    ]

    NameFiles = [
        'Recomendaciones para una Alimentación Saludable',
        'Servicio de Alimentación Guía 2025',
    ]
    FullNameFiles = [f'{name_file.replace(' ','-')}.pdf' for name_file in NameFiles]

    LastUpdates = [
        '2016/11',
        '2026/01',
    ]

    for link_file , name_file , last_update in zip(LinkFiles,FullNameFiles,LastUpdates):
        DownloadPDF(link_file,'https://www.gob.mx/sep',base_path/name_file)
        metadata_file = {
            'Title': name_file.replace('-',' ')[:-4],
            'Last Update': last_update,
            'Source': link_file,
            'File Name': name_file,
        }

        ListMetadata.append(metadata_file)

    DumpMetadata(ListMetadata,base_path/'metadata.json')
    return ListMetadata