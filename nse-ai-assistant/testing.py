import asyncio
import json

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


NSE_URL = "https://mcp.nseindia.in/bhavcopy/cm/mcp"


async def main():

    async with streamable_http_client(NSE_URL) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            result = await session.call_tool(
                "get_bulk_quote",
                {
                    "symbols": ["CYIENT"]
                }
            )

            # Get JSON text from MCP response
            data = json.loads(result.content[0].text)

            print("\nParsed response:\n")
            print(data)


asyncio.run(main())
