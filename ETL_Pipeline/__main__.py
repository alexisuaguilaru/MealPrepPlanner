import asyncio
import logging

from ETL_Pipeline import MainBEDCA , MainDatasetPricesPROFECO , MainAllrecipes , MainKiwilimon 
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

    _logger.info('Start Ingredients Prices from PROFECO')
    MainDatasetPricesPROFECO()

    _logger.info('Start Web Scraping of Ingredients from BEDCA')
    ingredients_bedca = MainBEDCA()

    _logger.info('Start Web Scraping of Recipes from Allrecipes')
    recipes_allrecipes = MainAllrecipes()

    _logger.info('Start Web Scraping of Recipes from Kiwilimon')
    recipes_kiwlimon = MainKiwilimon(5)

    _logger.info('No issues found')
    _logger.info('End Web Scraping')