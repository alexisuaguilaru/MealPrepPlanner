from crawl4ai import AsyncWebCrawler , CrawlerRunConfig , CrawlResult , JsonCssExtractionStrategy
import json

async def MainScrapeRecipesFromCuisine(CuisineLink: str):
    ExtractionSchema = {
        'name': 'Recipes from a Cuisine',
        'baseSelector': 'a.comp.mntl-card-list-items.mntl-universal-card.mntl-document-card.mntl-card.card.card--no-image',
        'fields': [
            {'name': 'Recipe Name', 'selector': 'span.card__title-text', 'type': 'text'},
            {'name': 'Link', 'type': 'attribute', 'attribute': 'href'}
        ]
    }

    CrawlerConfig = CrawlerRunConfig(
        extraction_strategy = JsonCssExtractionStrategy(ExtractionSchema),
    )

    async with AsyncWebCrawler() as crawler:
        result: CrawlResult  = await crawler.arun(
            url = CuisineLink,
            config = CrawlerConfig,
        )
        
    return json.loads(result.extracted_content)