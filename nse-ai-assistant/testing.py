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
                "get_stock_history",
                {
                    "symbol": "CYIENT",
                    "start_date": "2026-07-01",
                    "end_date": "2026-10-01"
                }
            )

            data = json.loads(result.content[0].text)

            print("\nHistorical data:\n")
            print(data)


asyncio.run(main())
