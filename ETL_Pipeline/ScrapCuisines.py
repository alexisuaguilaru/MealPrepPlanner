from crawl4ai import AsyncWebCrawler , CrawlerRunConfig , CrawlResult , JsonCssExtractionStrategy

async def MainScrapCuisines():
    ExtractionSchema = {
        'name': 'Cuisines',
        'baseSelector': 'li.comp.mntl-link-list__item',
        'fields': [
            {'name': 'Title', 'selector': 'a', 'type': 'text'},
            {'name': 'Link', 'selector': 'a', 'type': 'attribute', 'attribute': 'href'},
        ]
    }

    CrawlerConfig = CrawlerRunConfig(
        extraction_strategy = JsonCssExtractionStrategy(ExtractionSchema),
    )

    async with AsyncWebCrawler() as crawler:
        result: CrawlResult  = await crawler.arun(
            url = "https://www.allrecipes.com/cuisine-a-z-6740455",
            config = CrawlerConfig,
        )
        print(result.extracted_content)