import asyncio
import random
import json
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig , CrawlResult , BrowserConfig 

from ...Utils import BasicCrawlerRunConfig , BasicBrowserConfig

async def MainInteraction(PageLink):
    InteractionCode = f"""
    ( async () => {{
        const iframe = document.querySelector('iframe');
        const iframe_doc = iframe.contentDocument || iframe.contentWindow.document;

        const select_market = iframe_doc.querySelector('select#ddlDestinoMensual');
        const market_option = select_market.querySelector("option[value='160']");
        market_option.setAttribute('selected',true);

        const btn_submit = iframe_doc.querySelector('input#btnBuscarMensual');
        btn_submit.click();

        await new Promise(r => setTimeout(r, 2000));

        const iframe_data = document.querySelector('iframe');
        const iframe_data_doc = iframe_data.contentDocument || iframe_data.contentWindow.document;

        const table_data = iframe_data_doc.querySelector('table#tblResultados');

        const data = {{
            table_html: table_data.outerHTML
        }}

        console.log('__CRAWL4AI_RESULT__:' + JSON.stringify(data));
    }})();
    """

    Browser = BrowserConfig(
        **BasicBrowserConfig,
    )

    CrawlerConfig = CrawlerRunConfig(
        js_code = InteractionCode,
        **BasicCrawlerRunConfig,
        capture_console_messages = True,
    )

    async with AsyncWebCrawler(config=Browser) as crawler:
        result: CrawlResult  = await crawler.arun(
            url = PageLink,
            config = CrawlerConfig,
        )
        
        if result.console_messages:
            for msg in result.console_messages:
                text = msg.get('text', '')
                if text.startswith('__CRAWL4AI_RESULT__:'):
                    json_part = text.replace('__CRAWL4AI_RESULT__:', '')
                    json_html = json.loads(json_part)

                    await asyncio.sleep(random.uniform(2, 5))
                    return json_html['table_html']