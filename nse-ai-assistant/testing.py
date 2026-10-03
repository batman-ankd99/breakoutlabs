import asyncio
import json

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


NSE_URL = "https://mcp.nseindia.in/bhavcopy/cm/mcp"


async def get_stock_history(symbol, months=3, end_date="today"):

    all_records = []

    remaining_months = months

    while remaining_months > 0:

        chunk_months = min(3, remaining_months)

        async with streamable_http_client(NSE_URL) as (read, write):

            async with ClientSession(read, write) as session:

                await session.initialize()

                result = await session.call_tool(
                    "get_stock_history",
                    {
                        "symbol": symbol,
                        "months": chunk_months,
                        "endDate": end_date
                    }
                )

                if result.is_error:
                    print("NSE MCP returned an error:")
                    print(result.content)
                    return None

                data = json.loads(result.content[0].text)

                all_records = data["data"] + all_records

                end_date = data["next_end_date"]

        remaining_months -= chunk_months

    return all_records


async def main():

    records = await get_stock_history(
        "CYIENT",
        6
    )

    if records is None:
        return

    print("\n==============================")
    print("STOCK HISTORY")
    print("==============================")

    print("Total records:", len(records))

    print("\nOldest record:")
    print(records[0])

    print("\nNewest record:")
    print(records[-1])


asyncio.run(main())
