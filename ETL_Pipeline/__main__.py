import asyncio
import logging

from ETL_Pipeline import MainBEDCA , MainDatasetINSP , MainDatasetPricesPROFECO , MainDatasetPricesSNIIM , MainAllrecipes , MainKiwilimon , MainEatRight
from .Logger import ColorFormatter

_logger = logging.getLogger(' WEB SCRAPING ')
_logger.propagate = False
    
handler_cli = logging.StreamHandler()
handler_cli.setFormatter(ColorFormatter())
_logger.addHandler(handler_cli)

logging.basicConfig(level = logging.INFO)

if __name__ == '__main__':
    _logger.info('No issues with imports')
    _logger.info('Start Web Scraping')

    _logger.info('Start Web Scraping of Ingredients from BEDCA')
    # ingredients_bedca = MainBEDCA()
    # list(ingredients_bedca)

    _logger.info('Start Web Scraping of Ingredients from INSP: BAM')
    # ingredients_insp = MainDatasetINSP()

    _logger.info('Start Ingredients Prices from PROFECO')
    # ingredients_profeco = MainDatasetPricesPROFECO()

    _logger.info('Start Ingredients Prices from SNIIM')
    ingredients_sniim = MainDatasetPricesSNIIM()
    list(ingredients_sniim)

    _logger.info('Start Web Scraping of Recipes from Allrecipes')
    # recipes_allrecipes = MainAllrecipes()
    # list(recipes_allrecipes)

    _logger.info('Start Web Scraping of Recipes from Kiwilimon')
    # recipes_kiwlimon = MainKiwilimon(5)
    # list(recipes_kiwlimon)

    _logger.info('Start Web Scraping of Recipes from EatRight')
    # recipes_eatright = MainEatRight()
    # list(recipes_eatright)

    _logger.info('No issues found')
    _logger.info('End Web Scraping')