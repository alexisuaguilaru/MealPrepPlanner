from pathlib import Path
import asyncio

from .ScrapeListTechniques import MainScrapeTechniques
from .ScrapeTechniqueContent import MainScrapeTechniqueContent

from ...Utils import DumpMetadata , SaveMarkdownFile

def MainScraping(NumClicks):    
    BasePath = './Datasets/Documents/Larousse'
    base_path = Path(BasePath)
    base_path.mkdir(parents=True,exist_ok=True)

    ListMetadata = []

    for metadata_article in asyncio.run(MainScrapeTechniques(NumClicks)):
        route_name_2 , route_name_1 = metadata_article['Link'].split('/')[-2:]

        scraped_content = asyncio.run(MainScrapeTechniqueContent(metadata_article['Link']))

        file_name = (route_name_1 if route_name_1 else route_name_2) + '.md'
        metadata = {
            'Title': metadata_article['Title'],
            'Last Update': '',
            'Source': metadata_article['Link'],
            'File Name': file_name,
        }
        ListMetadata.append(metadata)

        SaveMarkdownFile(scraped_content,base_path/file_name)

    DumpMetadata(ListMetadata,base_path/'metadata.json')
    return ListMetadata