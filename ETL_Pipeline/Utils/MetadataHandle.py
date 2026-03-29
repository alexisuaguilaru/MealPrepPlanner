import json
from datetime import datetime

def DumpMetadata(Metadata,MetadataFile):
    with open(MetadataFile,'w',encoding='utf-8') as metadata_file:
        json.dump(Metadata,metadata_file,indent=4,ensure_ascii=False)

def CreateMetadataFromSources(LinkSources,FileNames,Date = datetime.today()):
    Metadata = []
    for link_page , file_name in zip(LinkSources,FileNames):
        metadata_entry = {
            'File Name': file_name,
            'Source': link_page,
            'Last Update': str(Date).split()[0].replace('-','/'),
        },
        Metadata.append(metadata_entry)
    return Metadata