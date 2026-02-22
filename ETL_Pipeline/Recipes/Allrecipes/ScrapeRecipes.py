import asyncio
import random
import json
from crawl4ai import AsyncWebCrawler , BrowserConfig , CrawlerRunConfig , CrawlResult , JsonCssExtractionStrategy

from ...Utils import BasicBrowserConfig , BasicCrawlerRunConfig

async def MainScrapeRecipesFromCuisine(CuisineLink: str):
    ExtractionSchema = {
        'name': 'Recipes from a Cuisine',
        'baseSelector': 'a.comp.mntl-card-list-items.mntl-universal-card.mntl-document-card.mntl-card.card.card--no-image',
        'fields': [
            {'name': 'Recipe Name', 'selector': 'span.card__title-text', 'type': 'text'},
            {'name': 'Link', 'type': 'attribute', 'attribute': 'href'}
        ]
    }

    Browser = BrowserConfig(
        **BasicBrowserConfig,
    )

    CrawlerConfig = CrawlerRunConfig(
        extraction_strategy = JsonCssExtractionStrategy(ExtractionSchema),
        **BasicCrawlerRunConfig,
    )

    async with AsyncWebCrawler(config=Browser) as crawler:
        result: CrawlResult  = await crawler.arun(
            url = CuisineLink,
            config = CrawlerConfig,
        )

    await asyncio.sleep(random.uniform(2, 5))   
    return json.loads(result.extracted_content)