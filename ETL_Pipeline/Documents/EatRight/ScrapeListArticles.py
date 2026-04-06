import asyncio
import random
from crawl4ai import AsyncWebCrawler , CrawlerRunConfig , CrawlResult , BrowserConfig , JsonCssExtractionStrategy , CacheMode
import json

from ...Utils import BasicCrawlerRunConfig , BasicBrowserConfig

async def MainScrapeListArticlesLinks(LinkTopic,NumClicks):
    SessionID = 'Session_Articles_EatRight'

    LoadMoreArticles = f"""
    (async () => {{
        const maxClicks = {NumClicks};
        const delayMs = 2000;
        const selectorButton = 'button.button.button--outline.article-listing__cta';

        for (let i = 0; i < maxClicks; i++) {{
            const button = document.querySelector(selectorButton);

            if (button) {{
                button.click();
                await new Promise(resolve => setTimeout(resolve, delayMs));
            }} else {{
                break;
            }}
        }}
    }})();
    """

    ExtractionSchema = {
        'name': 'List of Articles',
        'baseSelector': 'div.article-listing__container article',
        'fields': [
            {'name': 'Title', 'selector': 'h3', 'type': 'text'},
            {'name': 'Link', 'selector': 'a', 'type': 'attribute', 'attribute': 'href'},
        ]
    }

    Browser = BrowserConfig(
        **BasicBrowserConfig,
    )

    CrawlerRunConfig_EatRight = BasicCrawlerRunConfig.copy()
    del CrawlerRunConfig_EatRight['wait_until']
    CrawlerConfig = CrawlerRunConfig(
        extraction_strategy = JsonCssExtractionStrategy(ExtractionSchema),
        js_code = LoadMoreArticles,
        session_id = SessionID,
        **CrawlerRunConfig_EatRight,
        scan_full_page = True,
        max_scroll_steps = 2,
        cache_mode = CacheMode.ENABLED,
    )

    async with AsyncWebCrawler(config=Browser) as crawler:
        result: CrawlResult  = await crawler.arun(
            url = LinkTopic,
            config = CrawlerConfig,
        )
    
    await asyncio.sleep(random.uniform(3, 5))
    return json.loads(result.extracted_content)