import asyncio
import json

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


NSE_URL = "https://mcp.nseindia.in/bhavcopy/cm/mcp"


async def get_stock_history(symbol, months=3, end_date="today"):

    async with streamable_http_client(NSE_URL) as (read, write):

        async with ClientSession(read, write) as session:

            # Initialize MCP session
            await session.initialize()

            # Call NSE MCP tool
            result = await session.call_tool(
                "get_stock_history",
                {
                    "symbol": symbol,
                    "months": months,
                    "endDate": end_date
                }
            )

            # Check for MCP error
            if result.is_error:
                print("NSE MCP returned an error:")
                print(result.content)
                return None

            # Convert JSON string into Python dictionary
            data = json.loads(result.content[0].text)

            return data


async def main():

    data = await get_stock_history(
        symbol="CYIENT",
        months=3,
        end_date="2026-10-01"
    )

    if data is None:
        return

    print("\n==============================")
    print("STOCK HISTORY")
    print("==============================")

    print("Symbol:", data["symbol"])
    print("From:", data["from_date"])
    print("To:", data["to_date"])
    print("Trading days:", data["trading_days"])

    print("\n==============================")
    print("SUMMARY")
    print("==============================")

    summary = data["summary"]

    print("Period low:", summary["period_low"])
    print("Period high:", summary["period_high"])
    print("First close:", summary["first_close"])
    print("Last close:", summary["last_close"])
    print("Return %:", summary["return_pct"])
    print("Average volume:", summary["avg_daily_vol"])

    print("\n==============================")
    print("DAILY DATA")
    print("==============================")

    records = data["data"]

    print("Number of records:", len(records))

    print("\nFirst record:")
    print(records[0])

    print("\nLast record:")
    print(records[-1])

    print("\nNext end date:", data["next_end_date"])


asyncio.run(main())
