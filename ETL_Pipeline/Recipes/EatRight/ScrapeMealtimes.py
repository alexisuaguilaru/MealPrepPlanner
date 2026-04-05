import asyncio
import random
import json
from crawl4ai import AsyncWebCrawler , BrowserConfig , CrawlerRunConfig , CrawlResult , JsonCssExtractionStrategy , CacheMode

from ...Utils import BasicBrowserConfig , BasicCrawlerRunConfig

async def MainScrapeMealtimes():
    SessionID = 'Scrape_Mealtimes_EatRight'

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

    CrawlerConfig = CrawlerRunConfig(
        extraction_strategy = JsonCssExtractionStrategy(ExtractionSchema),
        session_id = SessionID,
        delay_before_return_html = random.uniform(3,5),
        scroll_delay = random.uniform(0.5,1),
        cache_mode = CacheMode.ENABLED,
    )

    async with AsyncWebCrawler(config=Browser) as crawler:
        result: CrawlResult  = await crawler.arun(
            url = 'https://www.eatright.org/recipes',
            config = CrawlerConfig,
        )

    await asyncio.sleep(random.uniform(3,5))   
    return json.loads(result.extracted_content)