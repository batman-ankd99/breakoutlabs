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

            data = json.loads(result.content[0].text)

            quote = data["quotes"][0]

            print("Symbol:", quote["symbol"])
            print("Price:", quote["close"])
            print("Change:", quote["pct_change"], "%")
            print("Volume:", quote["volume"])
            print("Date:", quote["date"])


asyncio.run(main())
