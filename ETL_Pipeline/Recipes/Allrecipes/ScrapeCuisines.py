import asyncio
import random
import json
from crawl4ai import AsyncWebCrawler , BrowserConfig , CrawlerRunConfig , CrawlResult , JsonCssExtractionStrategy

from ...Utils import BasicBrowserConfig , BasicCrawlerRunConfig

async def MainScrapeCuisines():
    ExtractionSchema = {
        'name': 'Cuisines',
        'baseSelector': 'li.comp.mntl-link-list__item',
        'fields': [
            {'name': 'Cuisine', 'selector': 'a', 'type': 'text'},
            {'name': 'Link', 'selector': 'a', 'type': 'attribute', 'attribute': 'href'},
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
            url = "https://www.allrecipes.com/cuisine-a-z-6740455",
            config = CrawlerConfig,
        )
    
    await syncio.sleep(random.uniform(2, 5))
    return json.loads(result.extracted_content)