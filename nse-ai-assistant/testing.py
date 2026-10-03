import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


NSE_URL = "https://mcp.nseindia.in/bhavcopy/cm/mcp"


async def main():

    async with streamable_http_client(NSE_URL) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            result = await session.call_tool(
                "nse_lookup_symbol",
                {
                    "query": "CYIENT"
                }
            )

            print("\nNSE Response:\n")
            print(result)


asyncio.run(main())
