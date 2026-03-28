import asyncio
import random
import json
from crawl4ai import AsyncWebCrawler , BrowserConfig , CrawlerRunConfig , CrawlResult , JsonCssExtractionStrategy

from ...Utils import BasicBrowserConfig , BasicCrawlerRunConfig

async def MainScrapeTable(Table):
    ExtractionSchema = {
        'name': 'List of Prices',
        'baseSelector': 'tr',
        'fields': [
            {'name': 'row', 'selector': 'td', 'type': 'list', 'fields': [
                {'name': 'entry', 'type': 'text'}
            ]},
        ],
    }

    Browser = BrowserConfig(
        headless = False,
    )

    CrawlerConfig_SNIIM = BasicCrawlerRunConfig.copy() 
    del CrawlerConfig_SNIIM['wait_until']
    CrawlerConfig = CrawlerRunConfig(
        extraction_strategy = JsonCssExtractionStrategy(ExtractionSchema),
        **CrawlerConfig_SNIIM,
        wait_for = 'css:table',
    )

    async with AsyncWebCrawler(config=Browser) as crawler:
        result: CrawlResult  = await crawler.arun(
            url = 'raw://'+Table,
            config = CrawlerConfig,
        )
 
    return json.loads(result.extracted_content)
