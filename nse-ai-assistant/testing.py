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

    # First 3 months
    data1 = await get_stock_history(
        "CYIENT",
        3,
        "2026-10-01"
    )

    # Previous 3 months
    data2 = await get_stock_history(
        "CYIENT",
        3,
        data1["next_end_date"]
    )

    print("\n==============================")
    print("FIRST CHUNK")
    print("==============================")

    print("From:", data1["from_date"])
    print("To:", data1["to_date"])
    print("Records:", len(data1["data"]))

    print("\n==============================")
    print("SECOND CHUNK")
    print("==============================")

    print("From:", data2["from_date"])
    print("To:", data2["to_date"])
    print("Records:", len(data2["data"]))

    print("\n==============================")
    print("TOTAL")
    print("==============================")

    all_records = data2["data"] + data1["data"]

    print("Total records:", len(all_records))

    print("\nOldest record:")
    print(all_records[0])

    print("\nNewest record:")
    print(all_records[-1])


asyncio.run(main())
