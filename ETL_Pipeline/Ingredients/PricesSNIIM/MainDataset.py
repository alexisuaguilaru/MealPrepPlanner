import asyncio
from pathlib import Path

from .InteractWithIFrames import MainInteraction
from .ScrapeDataTable import MainScrapeTable
from .ProcessTable import MainProcessJsonTable

from .MainExtraction import MainExtractionAgricultural

from ...Utils import DumpMetadata , CreateMetadataFromSources

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

    ListDatasets_Agricultural = MainExtractionAgricultural(MarketCategories['Agricultural'],dataset_path)
    Metadata_Agricultural = CreateMetadataFromSources(MarketCategories['Agricultural'],ListDatasets_Agricultural)
    DumpMetadata(Metadata_Agricultural,dataset_path/'metadata_agricultural.json')

    ListDatasets += ListDatasets_Agricultural

    return ListDatasets