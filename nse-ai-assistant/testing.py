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
                    "months": 3,
                    "endDate": "2026-10-01"
                  }
            )

            print("is_error:", result.is_error)
            print(result.content)

            print("\nRAW NSE RESPONSE:\n")

            data = json.loads(result.content[0].text)

            print("\nNumber of records:", len(data["history"]))

            print("\nFirst record:")
            print(data["history"][0])

            print("\nLast record:")
            print(data["history"][-1])

            print("\nNext end date:", data["next_end_date"])


asyncio.run(main())
