import asyncio

from .InteractWithIFrames import MainInteraction
from .ScrapeDataTable import MainScrapeTable
from .ProcessTable import MainProcessJsonTable

def MainExtractionAgricultural(LinkPagesAgricultural,DatasetPath):
    ListDatasets = []
    for page_link_Agricultural in LinkPagesAgricultural:
        html_table_Agricultural = asyncio.run(MainInteraction(page_link_Agricultural))
        json_table_Agricultural = asyncio.run(MainScrapeTable(html_table_Agricultural))
        table_Agricultural = MainProcessJsonTable(json_table_Agricultural)
        
        table_name_Agricultural = page_link_Agricultural.split('/')[-1][:-5]
        ListDatasets.append(f'{table_name_Agricultural}.csv')

        table_Agricultural.to_csv(DatasetPath/ListDatasets[-1])

    return ListDatasets