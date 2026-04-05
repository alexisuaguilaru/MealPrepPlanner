import asyncio
import random
import json
from crawl4ai import AsyncWebCrawler , BrowserConfig , CrawlerRunConfig , CrawlResult , JsonCssExtractionStrategy , CacheMode

from ...Utils import BasicBrowserConfig , BasicCrawlerRunConfig

async def MainScrapeRecipesMealtime(MealtimeLink: str):
    SessionID = 'Scrape_Mealtimes_EatRight'
    
    ExtractionSchema = {
        'name': 'List of Recipes from Mealtime',
        'baseSelector': 'div.article-listing__container article.card.card--clickable',
        'fields': [
            {'name': 'Recipe Name', 'selector': 'h3.card__heading', 'type': 'text'},
            {'name': 'Recipe Image', 'selector': 'img', 'type': 'attribute', 'attribute': 'src'},
            {'name': 'Link', 'selector': 'a.link-button.card__primary-link', 'type': 'attribute', 'attribute': 'href'},
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
            url = MealtimeLink,
            config = CrawlerConfig,
        )

    await asyncio.sleep(random.uniform(2, 5))   
    return json.loads(result.extracted_content)