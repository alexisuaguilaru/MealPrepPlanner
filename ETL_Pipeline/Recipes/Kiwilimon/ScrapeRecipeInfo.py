import asyncio
import random
import json
from crawl4ai import AsyncWebCrawler , BrowserConfig , CrawlerRunConfig , CrawlResult , JsonCssExtractionStrategy

from ...Utils import BasicBrowserConfig , BasicCrawlerRunConfig

async def MainScrapeRecipeInformation(RecipeLink: str):
    SessionID = 'Session_RecipeInformation_Kiwilimon'

    ExtractionSchema_Times = {
        'name': 'Recipe Information about Times',
        'baseSelector': 'div.recipe-area-info-receta',
        'fields': [
            {'name': 'Preparation Time', 'selector': 'div.icon-k7-receta-tpreparacion', 'type': 'text', 'default': '0 mins'},
            {'name': 'Cooking Time', 'selector': 'div.icon-k7-receta-tcocinar', 'type': 'text', 'default': '0 mins'},
        ]
    }

    ExtractionSchema_ServingsIngredients = {
        'name': 'Recipe Information about Servings and Ingredients',
        'baseSelector': 'div.recipe-intro-receta-normal',
        'fields': [
            {'name': 'Servings', 'selector': 'div.recipe-area-titulo-ingredientes-recnormal span', 'type': 'text', 'default': '1'},
            {'name': 'Ingredients', 'selector': 'div#ingredients-original label', 'type': 'list', 'fields':[
                {'name': 'ingredient', 'type': 'text'},
            ]},
        ]
    }

    ExtractionSchema_Directions = {
        'name': 'Recipe Information about Directions',
        'baseSelector': 'div.recipe-intro-data-pasos-normal',
        'fields': [
            {'name': 'Steps', 'selector': 'label', 'type': 'list', 'fields':[
                {'name': 'step', 'type': 'text'},
            ]}
        ]
    }

    BasicBrowserConfig_RecipeInfo = BasicBrowserConfig.copy()
    BasicBrowserConfig_RecipeInfo['user_agent_mode'] =  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    Browser = BrowserConfig(
        **BasicBrowserConfig_RecipeInfo,
        use_managed_browser = True,
    )

    CrawlerRunConfig_RecipeInfo = BasicCrawlerRunConfig.copy()
    del CrawlerRunConfig_RecipeInfo['wait_until']
    CrawlerConfig_RecipeInfo = CrawlerRunConfig(
        **CrawlerRunConfig_RecipeInfo,
        session_id = SessionID,
    )

    async with AsyncWebCrawler(config=Browser) as crawler:

        CrawlerConfig_RecipeInfo.extraction_strategy = JsonCssExtractionStrategy(ExtractionSchema_Times)
        result_Times: CrawlResult  = await crawler.arun(
            url = RecipeLink,
            config = CrawlerConfig_RecipeInfo,
        )

        CrawlerConfig_RecipeInfo.extraction_strategy = JsonCssExtractionStrategy(ExtractionSchema_ServingsIngredients)
        result_ServingsIngredients: CrawlResult  = await crawler.arun(
            url = RecipeLink,
            config = CrawlerConfig_RecipeInfo,
        )

        CrawlerConfig_RecipeInfo.extraction_strategy = JsonCssExtractionStrategy(ExtractionSchema_Directions)
        result_Directions: CrawlResult  = await crawler.arun(
            url = RecipeLink,
            config = CrawlerConfig_RecipeInfo,
        )

    Results = [
        result_Times,
        result_ServingsIngredients,
        result_Directions,
    ]
    await asyncio.sleep(random.uniform(2, 5))
    return [json.loads(result.extracted_content) for result in Results]