import asyncio
import random
import json
from crawl4ai import AsyncWebCrawler , BrowserConfig , CrawlerRunConfig , CrawlResult , JsonCssExtractionStrategy , VirtualScrollConfig

from ...Utils import BasicBrowserConfig , BasicCrawlerRunConfig

async def MainScrapeRecipesFromPage():
    ExtractionSchema = {
        'name': 'Recipes from Page',
        'baseSelector': 'div#tecuida-recipelist div.feed-receta-ficha',
        'fields': [
            {'name': 'Recipe Name', 'selector': 'div.feed-receta-nombreficha-centrado', 'type': 'text'},
            {'name': 'Link', 'selector': 'a', 'type': 'attribute', 'attribute': 'href'},
            {'name': 'Recipe Image', 'selector': 'img', 'type': 'attribute', 'attribute': 'src'},
        ]
    }

    Browser = BrowserConfig(
        **BasicBrowserConfig,
    )

    CrawlerConfig_Kiwilimon = BasicCrawlerRunConfig.copy()
    del CrawlerConfig_Kiwilimon['wait_until']
    CrawlerConfig = CrawlerRunConfig(
        extraction_strategy = JsonCssExtractionStrategy(ExtractionSchema),
        **CrawlerConfig_Kiwilimon,
        scan_full_page = True,
        max_scroll_steps = 5,
    )

    async with AsyncWebCrawler(config=Browser) as crawler:
        result: CrawlResult  = await crawler.arun(
            url = 'https://www.kiwilimon.com/te-cuida',
            config = CrawlerConfig,
        )

    await asyncio.sleep(random.uniform(2, 5))   
    return json.loads(result.extracted_content)