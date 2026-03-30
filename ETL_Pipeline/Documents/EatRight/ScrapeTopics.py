import asyncio
import random
from crawl4ai import AsyncWebCrawler , CrawlerRunConfig , CrawlResult , BrowserConfig , JsonCssExtractionStrategy , CacheMode
import json

from ...Utils import BasicCrawlerRunConfig , BasicBrowserConfig

async def MainScrapeListTopics(LinkPageEatRight):
    SessionID = 'Session_Articles_EatRight'

    ExtractionSchema = {
        'name': 'List of Topics',
        'baseSelector': 'article',
        'fields': [
            {'name': 'Title', 'selector': 'h3', 'type': 'text'},
            {'name': 'Link', 'selector': 'a', 'type': 'attribute', 'attribute': 'href'},
        ]
    }

    Browser = BrowserConfig(
        **BasicBrowserConfig,
    )

    CrawlerConfig = CrawlerRunConfig(
        extraction_strategy = JsonCssExtractionStrategy(ExtractionSchema),
        session_id = SessionID,
        **BasicCrawlerRunConfig,
        cache_mode = CacheMode.ENABLED,
    )

    async with AsyncWebCrawler(config=Browser) as crawler:
        result: CrawlResult  = await crawler.arun(
            url = LinkPageEatRight,
            config = CrawlerConfig,
        )
    
    await asyncio.sleep(random.uniform(3, 5))
    return json.loads(result.extracted_content)