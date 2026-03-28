import asyncio
from pathlib import Path

from .InteractWithIFrames import MainInteraction
from .ScrapeDataTable import MainScrapeTable
from .ProcessTable import MainProcessJsonTable

def MainDatasetETL():
    DatasetPath = './Datasets/IngredientsPrices/SNIIM'
    dataset_path = Path(DatasetPath)
    dataset_path.mkdir(parents=True,exist_ok=True)

    MarketCategories = {
        'Agricultural': [
            'http://www.economia-sniim.gob.mx/Nuevo/Home.aspx?opcion=Consultas/MercadosNacionales/PreciosDeMercado/Agricolas/ConsultaFrutasYHortalizas.aspx',
            'http://www.economia-sniim.gob.mx/Nuevo/Home.aspx?opcion=Consultas/MercadosNacionales/PreciosDeMercado/Agricolas/ConsultaFlores.aspx',
            'http://www.economia-sniim.gob.mx/Nuevo/Home.aspx?opcion=Consultas/MercadosNacionales/PreciosDeMercado/Agricolas/ConsultaGranos.aspx',
            'http://www.economia-sniim.gob.mx/Nuevo/Home.aspx?opcion=Consultas/MercadosNacionales/PreciosDeMercado/Agricolas/ConsultaAzucar.aspx',
            'http://www.economia-sniim.gob.mx/Nuevo/Home.aspx?opcion=Consultas/MercadosNacionales/PreciosDeMercado/Agricolas/ConsultaAceites.aspx',
        ],

        'Livestock': [
            'https://www.economia-sniim.gob.mx/SNIIM-Pecuarios-Nacionales/MenPec.asp?var=Bov',
            'https://www.economia-sniim.gob.mx/SNIIM-Pecuarios-Nacionales/MenPec.asp?var=Bec',
            'https://www.economia-sniim.gob.mx/SNIIM-Pecuarios-Nacionales/MenPec.asp?var=Por',
            'https://www.economia-sniim.gob.mx/SNIIM-Pecuarios-Nacionales/MenPec.asp?var=Cap',
            'https://www.economia-sniim.gob.mx/SNIIM-Pecuarios-Nacionales/MenPec.asp?var=Ovi',
            'https://www.economia-sniim.gob.mx/SNIIM-Pecuarios-Nacionales/MenAve.asp',
        ],

        'Fishing': [
            'https://www.economia-sniim.gob.mx/SNIIM-PESCA/MENUDEO1.ASP?tipo=PM',
            'https://www.economia-sniim.gob.mx/SNIIM-PESCA/MENUDEO1.ASP?tipo=CL',
            'https://www.economia-sniim.gob.mx/SNIIM-PESCA/MENUDEO1.ASP?tipo=MO',
            'https://www.economia-sniim.gob.mx/SNIIM-PESCA/MENUDEO1.ASP?tipo=PAD',
            'https://www.economia-sniim.gob.mx/SNIIM-PESCA/MENUDEO1.ASP?tipo=FIL',
            'https://www.economia-sniim.gob.mx/SNIIM-PESCA/e_enlata.asp?',
        ],
    }

    ListDatasets = []
    for page_link_Agricultural in MarketCategories['Agricultural']:
        html_table_Agricultural = asyncio.run(MainInteraction(page_link_Agricultural))
        json_table_Agricultural = asyncio.run(MainScrapeTable(html_table_Agricultural))
        table_Agricultural = MainProcessJsonTable(json_table_Agricultural)
        
        table_name_Agricultural = page_link_Agricultural.split('/')[-1][:-5]
        ListDatasets.append(dataset_path/f'{table_name_Agricultural}.csv')

        table_Agricultural.to_csv(ListDatasets[-1])

    return ListDatasets