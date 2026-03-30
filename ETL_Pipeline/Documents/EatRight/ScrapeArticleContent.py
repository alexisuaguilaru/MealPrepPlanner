import asyncio
import random
from crawl4ai import AsyncWebCrawler , CrawlerRunConfig , CrawlResult , BrowserConfig , JsonCssExtractionStrategy , CacheMode
import json

from ...Utils import BasicCrawlerRunConfig , BasicBrowserConfig

async def MainScrapeArticleContent(LinkArticle):
    ExtractionSchema = {
        'name': 'Information from Article',
        'baseSelector': 'body div',
        'fields': [
            {'name': 'Date 1', 'selector': 'div.article-detail-masthead__meta p:nth-child(2)', 'type': 'text'},
            {'name': 'Date 2', 'selector': 'div.article-detail-masthead__meta p:nth-child(3)', 'type': 'text'},
            {'name': 'Date 3', 'selector': 'div.article-detail-masthead__meta p:nth-child(4)', 'type': 'text'},
            {'name': 'HTML Content', 'selector': 'main section', 'type': 'html'}
        ]
    }

    Browser = BrowserConfig(
        **BasicBrowserConfig,
        java_script_enabled = False,
    )

    CrawlerRunConfig_EatRight = BasicCrawlerRunConfig.copy()
    CrawlerRunConfig_EatRight['wait_until']  = 'domcontentloaded'
    CrawlerConfig = CrawlerRunConfig(
        extraction_strategy = JsonCssExtractionStrategy(ExtractionSchema),
    )

    async with AsyncWebCrawler(config=Browser) as crawler:
        result: CrawlResult  = await crawler.arun(
            url = LinkArticle,
            config = CrawlerConfig,
        )

        for metadata_page in json.loads(result.extracted_content):
            if 2 <= len(metadata_page): break

        result_Content: CrawlResult  = await crawler.arun(
            url = 'raw://'+metadata_page['HTML Content'],
            config = CrawlerConfig,
        )

        del metadata_page['HTML Content']
    
    await asyncio.sleep(random.uniform(3, 5))
    return metadata_page , result_Content.markdown