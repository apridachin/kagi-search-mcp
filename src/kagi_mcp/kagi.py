from urllib.parse import urljoin

import httpx
from mcp import McpError, types as types

from kagi_mcp.config import Config

config = Config()


async def _call_kagi(
    method: str, url: str, params: dict | None = None, json: dict | None = None
) -> httpx.Response:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method,
                url=urljoin(config.KAGI_URL, url),
                headers={
                    "Authorization": f"Bot {config.KAGI_API_KEY}",
                    "Content-Type": "application/json",
                },
                params=params,
                json=json,
            )
            response.raise_for_status()

        return response

    except httpx.HTTPError as e:
        raise McpError(types.INTERNAL_ERROR, f"Kagi API error: {str(e)}")


async def ask_fastgpt(query: str) -> str:
    response = await _call_kagi(method="POST", url="fastgpt", json={"query": query})
    data = response.json()
    return data["data"]["output"]


async def enrich_web(query: str) -> str:
    response = await _call_kagi(
        method="GET",
        url="enrich/web",
        params={"q": query},
    )
    return response.text


async def enrich_news(query: str) -> str:
    response = await _call_kagi(
        method="GET",
        url="enrich/news",
        params={"q": query},
    )
    return response.text
