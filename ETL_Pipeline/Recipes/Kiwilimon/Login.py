import asyncio
import os
import json
from crawl4ai import AsyncWebCrawler , BrowserConfig , CrawlerRunConfig , CrawlResult , JsonCssExtractionStrategy , CacheMode

from ...Utils import BasicBrowserConfig , BasicCrawlerRunConfig

async def PerformLogin():
    SessionID = 'Session_RecipeInformation_Kiwilimon'

    BasicBrowserConfig_Login = BasicBrowserConfig.copy()
    BasicBrowserConfig_Login['user_agent_mode'] =  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    Browser = BrowserConfig(
        **BasicBrowserConfig_Login,
        use_managed_browser = True,
    )

    LoginEmail , LoginPassword = GetLoginCredentials()
    LoginCode = f"""
    const login = async () => {{
        
        const waitFor = (selector) => {{
            return new Promise(resolve => {{
                if (document.querySelector(selector)) return resolve(document.querySelector(selector));
                const observer = new MutationObserver(() => {{
                    if (document.querySelector(selector)) {{
                        resolve(document.querySelector(selector));
                        observer.disconnect();
                    }}
                }});
                observer.observe(document.body, {{ childList: true, subtree: true }});
            }});
        }};

        const LoginBtn = await waitFor("div.social-btn-nativo.kiwi");
        LoginBtn.click();

        await new Promise(r => setTimeout(r, 1000));
        
        const LoginEmailBtn = await waitFor("input#loginset-nativo-correo");
        const LoginPasswordBtn = await waitFor("input#loginset-nativo-contrasena");
        LoginEmailBtn.value = "{LoginEmail}";
        LoginPasswordBtn.value = "{LoginPassword}";

        await new Promise(r => setTimeout(r, 1000));

        const LoginSubmitBtn = await waitFor("button#loginset-nativo-submit");
        LoginSubmitBtn.removeAttribute('disabled');
        LoginSubmitBtn.click();

        await new Promise(r => setTimeout(r, 3000));
    }};
    await login();
    """

    CrawlerRunConfig_Login = BasicCrawlerRunConfig.copy()
    del CrawlerRunConfig_Login['wait_until']
    CrawlerConfig_Login = CrawlerRunConfig(
        **CrawlerRunConfig_Login,
        js_code = LoginCode,
        cache_mode = CacheMode.BYPASS,
        session_id = SessionID,
    )

    CrawlerRunConfig_Verify = BasicCrawlerRunConfig.copy()
    del CrawlerRunConfig_Verify['wait_until']
    CrawlerConfig_Verify = CrawlerRunConfig(
        **CrawlerRunConfig_Verify,
        cache_mode = CacheMode.BYPASS,
        session_id = SessionID,
    )

    async with AsyncWebCrawler(config=Browser) as crawler:
        result: CrawlResult = await crawler.arun(
            url = 'https://www.kiwilimon.com/mi-cuenta/perfil',
            config = CrawlerConfig_Verify,
        )

        if 'login' in result.redirected_url:
            result: CrawlResult = await crawler.arun(
                url = 'https://www.kiwilimon.com/login/social',
                config = CrawlerConfig_Login,
            )

def GetLoginCredentials():
    with open('./ETL_Pipeline/CREDENTIAL.json','r') as CredentialsFile:
        Credentials = json.load(CredentialsFile)
        return Credentials['Kiwilimon'].values()