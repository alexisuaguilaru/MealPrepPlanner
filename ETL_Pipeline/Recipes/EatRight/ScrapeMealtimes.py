import asyncio
import random
import json
from crawl4ai import AsyncWebCrawler , BrowserConfig , CrawlerRunConfig , CrawlResult , JsonCssExtractionStrategy

from ...Utils import BasicBrowserConfig , BasicCrawlerRunConfig

async def MainScrapeMealtimes():
    ExtractionSchema = {
        'name': 'List of Mealtimes',
        'baseSelector': 'article.card.card--clickable',
        'fields': [
            {'name': 'Mealtime', 'selector': 'h3.card__heading', 'type': 'text'},
            {'name': 'Link', 'selector': 'a.link-button.card__primary-link', 'type': 'attribute', 'attribute': 'href'}
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
            url = 'https://www.eatright.org/recipes',
            config = CrawlerConfig,
        )

    await asyncio.sleep(random.uniform(2, 5))   
    return json.loads(result.extracted_content)