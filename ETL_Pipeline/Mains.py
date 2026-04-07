import logging

from ETL_Pipeline import MainBEDCA , MainDatasetINSP , MainDatasetPricesPROFECO , MainDatasetPricesSNIIM 
from ETL_Pipeline import MainAllrecipes , MainKiwilimon , MainEatRight
from ETL_Pipeline import  MainWHO , MainINSP , MainSEP , MainDocumentsEatRight , MainLarousse

def MainExtraction(MainLogger: logging.Logger):
    MainLogger.info('Start Web Scraping & Downloads')

    MainLogger.info('Start Web Scraping of Ingredients from BEDCA')
    ingredients_bedca = MainBEDCA()
    list(ingredients_bedca)

    MainLogger.info('Start Web Scraping of Ingredients from INSP: BAM')
    ingredients_insp = MainDatasetINSP()

    MainLogger.info('Start Ingredients Prices from PROFECO')
    ingredients_profeco = MainDatasetPricesPROFECO()

    MainLogger.info('Start Ingredients Prices from SNIIM')
    ingredients_sniim = MainDatasetPricesSNIIM()
    list(ingredients_sniim)

    MainLogger.info('Start Web Scraping of Recipes from Allrecipes')
    recipes_allrecipes = MainAllrecipes()
    list(recipes_allrecipes)

    MainLogger.info('Start Web Scraping of Recipes from Kiwilimon')
    recipes_kiwlimon = MainKiwilimon(5)
    list(recipes_kiwlimon)

    MainLogger.info('Start Web Scraping of Recipes from EatRight')
    recipes_eatright = MainEatRight()
    list(recipes_eatright)

    MainLogger.info('Start Web Scraping of Pages from WHO')
    documents_who = MainWHO()
    list(documents_who)

    MainLogger.info('Start Downloading of Files from INSP')
    documents_insp = MainINSP()
    list(documents_insp)

    MainLogger.info('Start Downloading of Files from SEP')
    documents_sep = MainSEP()
    list(documents_sep)

    MainLogger.info('Start Web Scraping of Pages from EatRight')
    documents_eatright = MainDocumentsEatRight(2,3)
    list(documents_eatright)

    MainLogger.info('Start Web Scraping of Pages from Larousse')
    documents_larousse = MainLarousse(5)
    list(documents_larousse)

    MainLogger.info('End Web Scraping & Downloads')