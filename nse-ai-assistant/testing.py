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

            # Check if NSE returned an MCP error
            if result.is_error:
                print("NSE MCP returned an error:")
                print(result.content)
                return None

            # Convert MCP response text -> Python dictionary
            data = json.loads(result.content[0].text)

            return data


async def main():

    symbol = "CYIENT"

    # Get 3 months of history
    data = await get_stock_history(
        symbol=symbol,
        months=3,
        end_date="2026-10-01"
    )

    if data is None:
        return

    print("\n==============================")
    print("STOCK HISTORY")
    print("==============================")

    print("\nSymbol:")
    print(data["symbol"])

    print("\nFrom date:")
    print(data["from_date"])

    print("\nTo date:")
    print(data["to_date"])

    print("\nTrading days:")
    print(data["trading_days"])

    print("\nSource:")
    print(data["source"])

    print("\n==============================")
    print("SUMMARY")
    print("==============================")

    print("\nPeriod low:")
    print(data["summary"]["period_low"])

    print("\nPeriod high:")
    print(data["summary"]["period_high"])

    print("\nFirst close:")
    print(data["summary"]["first_close"])

    print("\nLast close:")
    print(data["summary"]["last_close"])

    print("\nReturn %:")
    print(data["summary"]["return_pct"])

    print("\nAverage daily volume:")
    print(data["summary"]["avg_daily_vol"])

    print("\n==============================")
    print("DAILY DATA")
    print("==============================")

    records = data["data"]

    print("\nNumber of records:")
    print(len(records))

    print("\nFirst record:")
    print(records[0])

    print("\nLast record:")
    print(records[-1])

    print("\n==============================")
    print("NEXT CHUNK")
    print("==============================")

    print("\nNext end date:")
    print(data["next_end_date"])


asyncio.run(main())
