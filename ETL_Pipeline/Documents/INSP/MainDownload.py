from pathlib import Path

from ...Utils import DownloadPDF , DumpMetadata

def MainDownloading():
    BasePath = './Datasets/Documents/INSP'
    base_path = Path(BasePath)
    base_path.mkdir(parents=True,exist_ok=True)

    ListMetadata = []

    LinkFiles = [
        'https://www.insp.mx/images/stories/2015/Noticias/Nutricion_y_Salud/Docs/151118_guias_alimentarias.pdf',
        'https://www.gob.mx/cms/uploads/attachment/file/1029510/Guias_Alimentarias_Mexico_2025.pdf',
    ]

    NameFiles = [
        'Guías Alimentarias y de Actividad Física',
        'Guías Alimentarias Saludables y Sostenibles para la Población Mexicana',
    ]
    FullNameFiles = [f'{name_file.replace(' ','-')}.pdf' for name_file in NameFiles]

    for link_file , name_file in zip(LinkFiles,FullNameFiles):
        DownloadPDF(link_file,'https://www.gob.mx',base_path/name_file)
        metadata_file = {
            'Title': name_file.replace('-',' ')[:-4],
            'Last Update': '2020/01/01',
            'Source': link_file,
            'File Name': name_file,
        }

        ListMetadata.append(metadata_file)

    DumpMetadata(ListMetadata,base_path/'metadata.json')
    return ListMetadata