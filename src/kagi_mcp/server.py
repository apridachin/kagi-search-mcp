import logging

import mcp.server.stdio
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions

from utils.config import Config
from kagi_mcp.kagi import ask_fastgpt, enrich_web, enrich_news

config = Config()
logging.basicConfig(level=config.LOG_LEVEL)
logger = logging.getLogger("kagi-mcp")
server = Server("kagi-mcp")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    pattern = r"^\s*(\b\w+\b\s*){1,3}$"
    return [
        types.Tool(
            name="ask_fastgpt",
            description="Ask fastgpt to search web and give an answer with references",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="enrich_web",
            description="Enrich context with web content focused on general, non-commercial web content.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "pattern": pattern},
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="enrich_news",
            description="Enrich context with web content focused on non-commercial news and discussions.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "pattern": pattern},
                },
                "required": ["query"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(
    name: str,
    arguments: dict,
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    tools = {
        "ask_fastgpt": ask_fastgpt,
        "enrich_web": enrich_web,
        "enrich_news": enrich_news,
    }
    if name not in tools.keys():
        raise ValueError(f"Unknown tool: {name}")

    if not arguments:
        raise ValueError("Missing arguments")

    query = arguments.get("query")

    if not query:
        raise ValueError("Missing query")

    tool_function = tools[name]
    result = await tool_function(query)

    return [
        types.TextContent(
            type="text",
            text=result,
        )
    ]


async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="kagi-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )
