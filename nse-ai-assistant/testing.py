import asyncio
import json

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


NSE_URL = "https://mcp.nseindia.in/bhavcopy/cm/mcp"


async def get_stock_history(symbol, months=3, end_date="today"):

    all_records = []
    remaining_months = months

    async with streamable_http_client(NSE_URL) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            while remaining_months > 0:

                chunk_months = min(3, remaining_months)

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


def calculate_metrics(records):

    start_price = records[0]["close"]
    end_price = records[-1]["close"]

    highest_price = max(record["high"] for record in records)
    lowest_price = min(record["low"] for record in records)

    average_volume = sum(
        record["volume"] for record in records
    ) / len(records)

    return_pct = (
        (end_price - start_price)
        / start_price
        * 100
    )

    peak = records[0]["close"]
    max_drawdown = 0

    for record in records:

        close = record["close"]

        if close > peak:
            peak = close

        drawdown = (
            (close - peak)
            / peak
            * 100
        )

        if drawdown < max_drawdown:
            max_drawdown = drawdown

    return {
        "start_price": start_price,
        "end_price": end_price,
        "return_pct": return_pct,
        "highest_price": highest_price,
        "lowest_price": lowest_price,
        "average_volume": average_volume,
        "max_drawdown": max_drawdown
    }


async def main():

    records = await get_stock_history(
        "CYIENT",
        6
    )

    if records is None:
        return

    metrics = calculate_metrics(records)

    print("\n==============================")
    print("STOCK HISTORY")
    print("==============================")

    print("Records:", len(records))
    print("From:", records[0]["date"])
    print("To:", records[-1]["date"])

    print("\n==============================")
    print("METRICS")
    print("==============================")

    print("Start price:", metrics["start_price"])
    print("End price:", metrics["end_price"])
    print("Return %:", round(metrics["return_pct"], 2))
    print("Highest price:", metrics["highest_price"])
    print("Lowest price:", metrics["lowest_price"])
    print("Average volume:", round(metrics["average_volume"]))
    print("Max drawdown %:", round(metrics["max_drawdown"], 2))


asyncio.run(main())
