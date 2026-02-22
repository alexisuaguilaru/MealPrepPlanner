import asyncio
import random
import json
from crawl4ai import AsyncWebCrawler , BrowserConfig , CrawlerRunConfig , CrawlResult , JsonCssExtractionStrategy

from ...Utils import BasicBrowserConfig_NoPersistentContext , BasicCrawlerRunConfig

async def MainScrapeIngredients():
    ExtractionSchema = {
        'name': 'List of Ingredients',
        'baseSelector': 'table#querytable1 tr',
        'fields': [
            {'name': 'Ingredient ID', 'selector': 'td', 'type': 'text'},
            {'name': 'Spanish Name', 'selector': 'td:nth-child(2)', 'type': 'text'},
            {'name': 'English Name', 'selector': 'td:nth-child(3)', 'type': 'text'},
        ]
    }

    Browser = BrowserConfig(
        **BasicBrowserConfig_NoPersistentContext,
    )

    CommandInteractions = [
        "document.querySelectorAll('a')[2]?.onclick();",
        "document.querySelector('a#Alfabetica')?.onclick();",
        "document.querySelector('div#alphabet a')?.onclick();",
    ]

    CrawlerConfig = CrawlerRunConfig(
        extraction_strategy = JsonCssExtractionStrategy(ExtractionSchema),
        js_code = CommandInteractions,
        wait_for = 'css:tr.row-b',
        **BasicCrawlerRunConfig,
    )

    async with AsyncWebCrawler(config=Browser) as crawler:
        result: CrawlResult  = await crawler.arun(
            url = 'https://www.bedca.net/bdpub/index.php',
            config = CrawlerConfig,
        )

    await asyncio.sleep(random.uniform(2, 5))
    return json.loads(result.extracted_content)