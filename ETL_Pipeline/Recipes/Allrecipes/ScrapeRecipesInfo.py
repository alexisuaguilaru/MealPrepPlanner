import asyncio
import random
import json
from crawl4ai import AsyncWebCrawler , BrowserConfig , CrawlerRunConfig , CrawlResult , JsonCssExtractionStrategy

from ...Utils import BasicBrowserConfig , BasicCrawlerRunConfig

async def MainScrapeRecipeInformation(RecipeLink: str):
    SessionID = 'Session_RecipeInformation_Allrecipes'

    ExtractionSchema_TimesServings = {
        'name': 'Recipe Information about Times and Serving',
        'baseSelector': 'div.mm-recipes-details__item',
        'fields': [
            {'name': 'Label', 'selector': '.mm-recipes-details__label', 'type': 'text'},
            {'name': 'Value', 'selector': '.mm-recipes-details__value', 'type': 'text'},
        ]
    }

    ExtractionSchema_Ingredients = {
        'name': 'Recipe Information about Ingredients and Quantities',
        'baseSelector': 'ul.mm-recipes-structured-ingredients__list',
        'fields': [
            {'name': 'Ingredients', 'selector': 'li', 'type': 'list', 'fields':[
                {'name': 'quantity','selector': 'span[data-ingredient-quantity="true"]','type': 'text', 'default': 0},
                {'name': 'unit','selector': 'span[data-ingredient-unit="true"]','type': 'text', 'default': ''},
                {'name': 'name','selector': 'span[data-ingredient-name="true"]','type': 'text', 'default': ''},
            ]},
        ]
    }

    ExtractionSchema_Directions = {
        'name': 'Recipe Information about Directions',
        'baseSelector': 'ol.comp.mntl-sc-block.mntl-sc-block-startgroup.mntl-sc-block-group--OL',
        'fields': [
            {'name': 'Steps', 'selector': 'li', 'type': 'list', 'fields':[{'name': 'step', 'type': 'text'}]},
        ]
    }

    ExtractionSchema_NutritionalFacts = {
        'name': 'Recipe Information about Nutritional Facts',
        'baseSelector': 'table.mm-recipes-nutrition-facts-label__table',
        'fields': [
            {'name': 'Calories', 'selector': 'tr.mm-recipes-nutrition-facts-label__calories span:nth-of-type(2)', 'type': 'text'},
            {'name': 'Nutritional Facts', 'selector': 'tbody tr:nth-child(n+2)', 'type': 'nested_list', 'fields':[
                {'name': 'label', 'selector': 'td span', 'type': 'text'},
                {'name': 'value', 'selector': 'td', 'type': 'regex', 'pattern': r'[A-Za-z ]+\s*([\d.]+\w+)'},
            ]}
        ]
    }

    ExtractionSchema_Images = {
        'name': 'Recipe Image',
        'baseSelector': 'div.loc.article-content',
        'fields': [
            {'name': 'Recipe Image', 'selector': 'figure img', 'type': 'attribute', 'attribute': 'src'},
            {'name': 'Recipe Image', 'selector': 'div#article__photo-ribbon_1-0 a img', 'type': 'attribute', 'attribute': 'src'},
        ]
    }

    Browser = BrowserConfig(
        **BasicBrowserConfig,
    )
    
    CrawlerConfig_AllRecipes = BasicCrawlerRunConfig.copy()
    del CrawlerConfig_AllRecipes['wait_until']
    CrawlerConfig = CrawlerRunConfig(
        session_id = SessionID,
        **CrawlerConfig_AllRecipes,
        scan_full_page = True,
        max_scroll_steps = 2,
    )

    async with AsyncWebCrawler(config=Browser) as crawler:

        CrawlerConfig.extraction_strategy = JsonCssExtractionStrategy(ExtractionSchema_TimesServings)
        result_TimesServings: CrawlResult  = await crawler.arun(
            url = RecipeLink,
            config = CrawlerConfig,
        )

        CrawlerConfig.extraction_strategy = JsonCssExtractionStrategy(ExtractionSchema_Ingredients)
        result_Ingredients: CrawlResult  = await crawler.arun(
            url = RecipeLink,
            config = CrawlerConfig,
        )

        await asyncio.sleep(random.uniform(2, 5))

        CrawlerConfig.extraction_strategy = JsonCssExtractionStrategy(ExtractionSchema_Directions)
        result_Directions: CrawlResult  = await crawler.arun(
            url = RecipeLink,
            config = CrawlerConfig,
        )

        CrawlerConfig.extraction_strategy = JsonCssExtractionStrategy(ExtractionSchema_NutritionalFacts)
        result_NutritionalFacts: CrawlResult  = await crawler.arun(
            url = RecipeLink,
            config = CrawlerConfig,
        )

        await asyncio.sleep(random.uniform(0.5,1))
        
        CrawlerConfig.extraction_strategy = JsonCssExtractionStrategy(ExtractionSchema_Images)
        result_Images: CrawlResult  = await crawler.arun(
            url = RecipeLink,
            config = CrawlerConfig,
        )

    Results = [
        result_TimesServings, 
        result_Ingredients, 
        result_Directions,
        result_NutritionalFacts,
        result_Images,
    ]
    await asyncio.sleep(random.uniform(2, 5))
    return [json.loads(result.extracted_content) for result in Results]