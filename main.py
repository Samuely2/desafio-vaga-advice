import asyncio
from config import NAMES, URL, DB_NAME, JSON_FILE
from scraper.browser import scrape_name
from storage.sqlite_manager import save_to_sqlite
from storage.json_manager import save_to_json

async def main():
    all_data = []
    for name in NAMES:
        print(f"Consultando: {name}")
        processes = await scrape_name(name, URL)
        all_data.append({"nome_busca": name, "processos": processes})
        await asyncio.sleep(5)
    
    save_to_json(all_data, JSON_FILE)
    save_to_sqlite(all_data, DB_NAME)

if __name__ == "__main__":
    asyncio.run(main())
