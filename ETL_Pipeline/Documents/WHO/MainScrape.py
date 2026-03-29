from pathlib import Path
import asyncio

from .ScrapeContent import MainScrapeContentFromPage

from ...Utils import SaveMarkdownFile , DumpMetadata

def MainScraping():
    BasePath = './Datasets/Documents/WHO'
    base_path = Path(BasePath)
    base_path.mkdir(parents=True,exist_ok=True)

    ListMetadata = []

    LinkPages = [
        'https://www.who.int/news-room/fact-sheets/detail/healthy-diet',
        'https://www.who.int/news-room/fact-sheets/detail/food-safety',
        'https://www.who.int/news-room/fact-sheets/detail/malnutrition',
        'https://www.who.int/news-room/fact-sheets/detail/obesity-and-overweight',
    ]

    for link_page_WHO in LinkPages:
        metadata_page , scraped_content = asyncio.run(MainScrapeContentFromPage(link_page_WHO))

        metadata_page['Source'] = link_page_WHO
        metadata_page['File Name'] = f'{metadata_page['Title'].replace(' ','-')}.md'
        ListMetadata.append(metadata_page)

        SaveMarkdownFile(scraped_content,base_path/metadata_page['File Name'])

    DumpMetadata(ListMetadata,base_path/'metadata.json')
    return ListMetadata