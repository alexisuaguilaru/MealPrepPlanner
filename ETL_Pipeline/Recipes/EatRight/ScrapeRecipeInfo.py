import asyncio
import random
import json
from crawl4ai import AsyncWebCrawler , BrowserConfig , CrawlerRunConfig , CrawlResult , JsonXPathExtractionStrategy

from ...Utils import BasicBrowserConfig , BasicCrawlerRunConfig

async def MainScrapeRecipeInformation(RecipeLink: str):
    ExtractionSchema = {
        'name': 'List of Mealtimes',
        'baseSelector': 'section.rtf',
        'fields': [
            {'name': 'Times', 'selector': ".//p[contains(text(),'minute') or contains(text(), 'hour')]", 'type': 'text', 'default': '0 minutes'},
            {'name': 'Ingredientes', 'selector': ".//h3[contains(text(),'Ingredient')]/following-sibling::p[1]", 'type': 'text'},
            {'name': 'Servings Nutritional Facts', 'selector': ".//h3[contains(text(), 'Nutrition')]/following-sibling::p", 'type': 'html'},
            {'name': 'Directions', 'selector': "//ol/li", 'type': 'list', 'fields': [{'name': 'direction', 'type': 'text'}]},
        ],
    }

    Browser = BrowserConfig(
        **BasicBrowserConfig,
    )

    CrawlerConfig_EatRight = BasicCrawlerRunConfig.copy()
    del CrawlerConfig_EatRight['wait_until']
    CrawlerConfig = CrawlerRunConfig(
        extraction_strategy = JsonXPathExtractionStrategy(ExtractionSchema),
        **CrawlerConfig_EatRight,
    )

    async with AsyncWebCrawler(config=Browser) as crawler:
        result: CrawlResult  = await crawler.arun(
            url = RecipeLink,
            config = CrawlerConfig,
        )

    await asyncio.sleep(random.uniform(2, 5))   
    return json.loads(result.extracted_content)