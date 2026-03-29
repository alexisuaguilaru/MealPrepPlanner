import json
import asyncio
import random

from crawl4ai import AsyncWebCrawler , BrowserConfig , CrawlerRunConfig , CrawlResult , JsonCssExtractionStrategy

from ...Utils import BasicBrowserConfig_NoPersistentContext , BasicCrawlerRunConfig

async def MainScrapeContentFromPage(LinkPage):
    ExtractionSchema = {
        'name': 'Information from WHO Page',
        'baseSelector': 'div#PageContent_T0643CD2A006_Col01',
        'fields': [
            {'name': 'Title', 'selector': 'h1', 'type': 'text'},
            {'name': 'Last Update', 'selector': 'div.date', 'type': 'text'},
        ]
    }

    Browser = BrowserConfig(
        **BasicBrowserConfig_NoPersistentContext,
    )

    CrawlerRunConfig_WHO = BasicCrawlerRunConfig.copy()
    del CrawlerRunConfig_WHO['wait_until']
    CrawlerConfig = CrawlerRunConfig(
        extraction_strategy = JsonCssExtractionStrategy(ExtractionSchema),
        **CrawlerRunConfig_WHO,
        css_selector = 'div#PageContent_T0643CD2A006_Col01',
    )

    async with AsyncWebCrawler(config=Browser) as crawler:
        result: CrawlResult  = await crawler.arun(
            url = LinkPage,
            config = CrawlerConfig,
        )
    
    await asyncio.sleep(random.uniform(2, 5))
    return json.loads(result.extracted_content)[0] , result.markdown