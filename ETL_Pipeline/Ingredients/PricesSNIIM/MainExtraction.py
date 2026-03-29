import asyncio

from .InteractWithIFrames import MainInteractionAgricultural , MainInteractionLivestock
from .ScrapeDataTable import MainScrapeTable
from .ProcessTable import MainProcessJsonTable

def MainExtractionAgricultural(LinkPagesAgricultural,DatasetPath):
    ListDatasets = []
    for page_link_Agricultural in LinkPagesAgricultural:
        html_table_Agricultural = asyncio.run(MainInteractionAgricultural(page_link_Agricultural))
        json_table_Agricultural = asyncio.run(MainScrapeTable(html_table_Agricultural))
        table_Agricultural = MainProcessJsonTable(json_table_Agricultural)
        
        table_name_Agricultural = page_link_Agricultural.split('/')[-1][:-5]
        ListDatasets.append(f'{table_name_Agricultural}.csv')

        table_Agricultural.to_csv(DatasetPath/ListDatasets[-1])

    return ListDatasets

def MainExtractionLivestock(LinkPagesLivestock,DatasetPath):
    SelectOptionValues = {
        'ConsultaBov': ('origen','16'),
        'ConsultaBec': ('destino','0'),
        'ConsultaPor': ('destino','16'),
        'ConsultaCap': ('destino','0'),
        'ConsultaOvi': ('destino','0'),
    }

    ListDatasets = []
    ListSources = []
    for page_link_Livestock in LinkPagesLivestock:
        table_name_Livestock = 'Consulta'+page_link_Livestock[-3:]
        json_tables_Livestock = asyncio.run(MainInteractionLivestock(page_link_Livestock,*SelectOptionValues[table_name_Livestock]))

        for index_table , json_table_Livestock in enumerate(json_tables_Livestock,1):
            table_Livestock = MainProcessJsonTable(json_table_Livestock['Table Data'])

            ListDatasets.append(f'{table_name_Livestock}_{index_table:02}.csv')
            ListSources.append(page_link_Livestock)

            table_Livestock.to_csv(DatasetPath/ListDatasets[-1])

    return ListSources , ListDatasets