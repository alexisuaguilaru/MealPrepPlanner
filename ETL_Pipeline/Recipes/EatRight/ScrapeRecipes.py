import asyncio
import random
import json
from crawl4ai import AsyncWebCrawler , BrowserConfig , CrawlerRunConfig , CrawlResult , JsonCssExtractionStrategy

from ...Utils import BasicBrowserConfig , BasicCrawlerRunConfig

async def MainScrapeRecipesMealtime(MealtimeLink: str):
    ExtractionSchema = {
        'name': 'List of Recipes from Mealtime',
        'baseSelector': 'div.article-listing__container article.card.card--clickable',
        'fields': [
            {'name': 'Recipe Name', 'selector': 'h3.card__heading', 'type': 'text'},
            {'name': 'Recipe Image', 'selector': 'img', 'type': 'attribute', 'attribute': 'src'},
            {'name': 'Link', 'selector': 'a.link-button.card__primary-link', 'type': 'attribute', 'attribute': 'href'},
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
            url = MealtimeLink,
            config = CrawlerConfig,
        )

    await asyncio.sleep(random.uniform(2, 5))   
    return json.loads(result.extracted_content)