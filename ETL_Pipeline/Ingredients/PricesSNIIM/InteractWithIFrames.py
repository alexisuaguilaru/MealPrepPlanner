import asyncio
import random
import json
from datetime import datetime
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig , CrawlResult , BrowserConfig , JsonCssExtractionStrategy

from ...Utils import BasicCrawlerRunConfig , BasicBrowserConfig

async def MainInteractionAgricultural(PageLink):
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

        return asyncio.run(ExtractTableHTMLFromMessages(result))
    
async def MainInteractionLivestock(PageLink,SelectionOption,OptionValue):
    day = datetime.today().day
    today_day = f'{max(0,day-8):02}'
    InteractionCode = f"""
    ( async () => {{
        const select_btn = document.querySelector("select[name='{SelectionOption}']");
        const value_option = select_btn.querySelector("option[value='{OptionValue}']");
        value_option.setAttribute('selected',true);

        const select_start_day = document.querySelector("select[name='del']");
        const start_day_option = select_start_day.querySelector("option[value='{today_day}']");
        start_day_option.setAttribute('selected',true);

        const btn_submit = document.querySelector("input[value='Buscar']");
        btn_submit.click();

        await new Promise(r => setTimeout(r, 2000));
    }})();
    """

    ExtractionSchema = {
        'name': 'List of Tables',
        'baseSelector': "table[border='1']",
        'fields': [
            {'name': 'Table Data', 'selector': 'tr', 'type': 'nested_list', 'fields': [
                {'name': 'row', 'selector': 'td', 'type': 'list', 'fields': [
                    {'name': 'entry', 'type': 'text'},
                ]},
            ]},
        ],
    }

    Browser = BrowserConfig(
        **BasicBrowserConfig,
    )

    CrawlerConfig = CrawlerRunConfig(
        extraction_strategy = JsonCssExtractionStrategy(ExtractionSchema),
        js_code = InteractionCode,
        **BasicCrawlerRunConfig,
        capture_console_messages = True,
    )

    async with AsyncWebCrawler(config=Browser) as crawler:
        result: CrawlResult  = await crawler.arun(
            url = PageLink,
            config = CrawlerConfig,
        )

        await asyncio.sleep(random.uniform(2, 5))
        return json.loads(result.extracted_content)
                
async def ExtractTableHTMLFromMessages(ResultScrape):
    if ResultScrape.console_messages:
        for msg in ResultScrape.console_messages:
            text = msg.get('text', '')
            if text.startswith('__CRAWL4AI_RESULT__:'):
                json_part = text.replace('__CRAWL4AI_RESULT__:', '')
                json_html = json.loads(json_part)

                await asyncio.sleep(random.uniform(2, 5))
                return json_html['table_html']
            
# def ExtractSeveralTablesHTMLFromMessages(ResultScrape):
#     TablesHTML = []
#     if ResultScrape.console_messages:
#         for msg in ResultScrape.console_messages:
#             text = msg.get('text', '')
#             if text.startswith('__CRAWL4AI_RESULT__:'):
#                 json_part = text.replace('__CRAWL4AI_RESULT__:', '')
#                 json_html = json.loads(json_part)
#     # TablesHTML.append(json_html[f'table_html_{index_table+1}'])
#     return TablesHTML