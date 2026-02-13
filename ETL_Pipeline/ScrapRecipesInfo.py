from crawl4ai import AsyncWebCrawler , CrawlerRunConfig , CrawlResult , JsonCssExtractionStrategy
import json

async def MainScrapRecipeInformation(RecipeLink: str):
    SessionID = 'Session_RecipeInformation'

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
            {'name': 'Ingredients', 'selector': 'li', 'type': 'list', 'fields':[{'name': 'ingredient','type': 'text'},]},
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

    CrawlerConfig = CrawlerRunConfig(
        session_id = SessionID,
    )

    async with AsyncWebCrawler() as crawler:

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

    Results = [
        result_TimesServings, 
        result_Ingredients, 
        result_Directions,
        result_NutritionalFacts,
    ]
    return [json.loads(result.extracted_content) for result in Results]