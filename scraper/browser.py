import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from .parser import parse_content

async def scrape_name(name, url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_load_state('networkidle')

        await page.fill('#txtStrParte', name)
        await page.click('#sbmNovo')
        await page.wait_for_load_state('networkidle')

        try:
            await page.click(f"#divInfraAreaTabela > table :text-is('{name}')")
            process_link_selector = "#divInfraAreaTabela > table > tbody > tr.infraTrClara > td:nth-child(1) a"
            await page.wait_for_selector(process_link_selector)
            await page.click(process_link_selector)
            await page.wait_for_selector("fieldset#fldPartes tr.infraTrClara:last-child", timeout=15000)
        except Exception as e:
            print(f"Aviso: Não foi possível carregar a página do processo para {name}. Erro: {e}")

        page_content = await page.content()
        soup = BeautifulSoup(page_content, 'html.parser')
        await browser.close()
        return parse_content(soup)
