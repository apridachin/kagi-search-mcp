import asyncio

from kagi_mcp.config import Config
from kagi_mcp.kagi import ask_fastgpt, enrich_web, enrich_news

config = Config()

if __name__ == "__main__":
    ask = asyncio.run(ask_fastgpt("current price of NVDA stock on NYSE"))
    enrich_web = asyncio.run(enrich_web("NVDA stock on NYSE"))
    enrich_news = asyncio.run(enrich_news("NVDA stock on NYSE"))
    print(json.dumps(ask, indent=2))
    print(json.dumps(enrich_news, indent=2))
    print(json.dumps(enrich_web, indent=2))
