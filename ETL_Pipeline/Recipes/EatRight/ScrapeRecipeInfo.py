import asyncio
import random
import json
from crawl4ai import AsyncWebCrawler , BrowserConfig , CrawlerRunConfig , CrawlResult , JsonCssExtractionStrategy

from ...Utils import BasicBrowserConfig , BasicCrawlerRunConfig

async def MainScrapeRecipeInformation(RecipeLink: str):
    ExtractionSchema = {
        'name': 'List of Mealtimes',
        'baseSelector': 'section.rtf',
        'fields': [
            {'name': 'Ingredients', 'selector': 'p:nth-of-type(2)', 'type': 'text'},
            {'name': 'Servings', 'selector': 'p:nth-of-type(4)', 'type': 'text'},
            {'name': 'Nutritional Facts', 'selector': 'p:nth-of-type(5)', 'type': 'text'},
            {'name': 'Directions', 'selector': 'ol li', 'type': 'list', 'fields': [{'name': 'direction', 'type': 'text'}]},
        ]
    }

    Browser = BrowserConfig(
        **BasicBrowserConfig,
    )

    CrawlerConfig_EatRight = BasicCrawlerRunConfig.copy()
    del CrawlerConfig_EatRight['wait_until']
    CrawlerConfig = CrawlerRunConfig(
        extraction_strategy = JsonCssExtractionStrategy(ExtractionSchema),
        **CrawlerConfig_EatRight,
    )

    async with AsyncWebCrawler(config=Browser) as crawler:
        result: CrawlResult  = await crawler.arun(
            url = RecipeLink,
            config = CrawlerConfig,
        )

    await asyncio.sleep(random.uniform(2, 5))   
    return json.loads(result.extracted_content)