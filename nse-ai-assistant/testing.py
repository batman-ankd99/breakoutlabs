import asyncio
import json

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


NSE_URL = "https://mcp.nseindia.in/bhavcopy/cm/mcp"


async def get_stock_history(symbol, months=3, end_date="today"):

    async with streamable_http_client(NSE_URL) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            result = await session.call_tool(
                "get_stock_history",
                {
                    "symbol": symbol,
                    "months": months,
                    "endDate": end_date
                }
            )

            if result.is_error:
                print("NSE MCP returned an error:")
                print(result.content)
                return None

            return json.loads(result.content[0].text)


async def main():

    all_records = []

    end_date = "2026-10-01"

    for i in range(2):

        data = await get_stock_history(
            "CYIENT",
            3,
            end_date
        )

        if data is None:
            return

        all_records = data["data"] + all_records

        end_date = data["next_end_date"]

    print("\n==============================")
    print("6 MONTH HISTORY")
    print("==============================")

    print("Total records:", len(all_records))

    print("\nOldest record:")
    print(all_records[0])

    print("\nNewest record:")
    print(all_records[-1])


asyncio.run(main())
