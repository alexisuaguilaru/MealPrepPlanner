import asyncio
import random
from crawl4ai import AsyncWebCrawler , CrawlerRunConfig , CrawlResult , BrowserConfig , JsonCssExtractionStrategy , CacheMode
import json

from ...Utils import BasicCrawlerRunConfig , BasicBrowserConfig

async def MainScrapeTechniques(NumClicks):
    SessionID = 'Session_Techniques_Larousse'

    LoadMoreTechniques = f"""
    (async () => {{
        const maxClicks = {NumClicks};
        const delayMs = 2000;
        const selectorButton = 'button.btn-ver-mas-rec-single';

        for (let i = 0; i < maxClicks; i++) {{
            const button = document.querySelector(selectorButton);

            if (button) {{
                button.click();
                await new Promise(resolve => setTimeout(resolve,delayMs));
            }} else {{
                break;
            }}
        }}

        await new Promise(resolve => setTimeout(resolve,10000));
    }})();
    """

    ExtractionSchema = {
        'name': 'List of Techniques',
        'baseSelector': 'div#bgs-blog-content div.card-item',
        'fields': [
            {'name': 'Title', 'selector': 'h3', 'type': 'text'},
            {'name': 'Link', 'selector': 'a', 'type': 'attribute', 'attribute': 'href'},
        ]
    }

    Browser = BrowserConfig(
        headless = False,
    )

    CrawlerConfig = CrawlerRunConfig(
        extraction_strategy = JsonCssExtractionStrategy(ExtractionSchema),
        js_code = LoadMoreTechniques,
        delay_before_return_html = 10,
        wait_until = 'domcontentloaded',
    )

    async with AsyncWebCrawler(config=Browser) as crawler:
        result: CrawlResult  = await crawler.arun(
            url = 'https://laroussecocina.mx/tecnicas/',
            config = CrawlerConfig,
        )
    
    await asyncio.sleep(random.uniform(3, 5))
    return json.loads(result.extracted_content)