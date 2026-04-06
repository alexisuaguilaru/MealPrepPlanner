import asyncio
import random
import json
from crawl4ai import AsyncWebCrawler , BrowserConfig , CrawlerRunConfig , CrawlResult , JsonCssExtractionStrategy , CacheMode

from ...Utils import BasicBrowserConfig , BasicCrawlerRunConfig

async def MainScrapeRecipeInformation(RecipeLink: str):
    SessionID = 'Session_RecipeInformation_Kiwilimon'

    ExtractionSchema = {
        'name': 'Recipe information',
        'baseSelector': 'body',
        'fields': [
            {'name': 'Preparation Time', 'selector': 'div.recipe-area-info-receta div.icon-k7-receta-tpreparacion', 'type': 'text', 'default': '0 mins'},
            {'name': 'Cooking Time', 'selector': 'div.recipe-area-info-receta div.icon-k7-receta-tcocinar', 'type': 'text', 'default': '0 mins'},
            {'name': 'Servings', 'selector': 'div.recipe-intro-receta-normal div.recipe-area-titulo-ingredientes-recnormal span', 'type': 'text', 'default': '1'},
            {'name': 'Ingredients', 'selector': 'div#ingredients-original label', 'type': 'list', 'fields': [{'name': 'ingredient', 'type': 'text'}]},
            {'name': 'Steps', 'selector': 'div.recipe-intro-data-pasos-normal label', 'type': 'list', 'fields': [{'name': 'step', 'type': 'text'}]}
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
        extraction_strategy = JsonCssExtractionStrategy(ExtractionSchema),
        session_id = SessionID,
        **CrawlerRunConfig_RecipeInfo,
    )

    async with AsyncWebCrawler(config=Browser) as crawler:

        result: CrawlResult = await crawler.arun(
            url = RecipeLink,
            config = CrawlerConfig_RecipeInfo,
        )

        await asyncio.sleep(random.uniform(3,5))
        try:
            return json.loads(result.extracted_content)[0]
        except:
            return {}