import asyncio
import json

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


NSE_URL = "https://mcp.nseindia.in/bhavcopy/cm/mcp"


async def get_stock_history(symbol, months=3, end_date="today"):

    all_records = []
    remaining_months = months
    corporate_actions = {}

    async with streamable_http_client(NSE_URL) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            # Get corporate actions
            result = await session.call_tool(
                "get_corporate_actions",
                {
                    "symbol": symbol
                }
            )

            if result.is_error:

                print("Corporate actions error:")
                print(result.content)

            else:

                corporate_actions = json.loads(
                    result.content[0].text
                )

            # Get historical data
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

                    return None, None

                data = json.loads(
                    result.content[0].text
                )

                all_records = data["data"] + all_records

                end_date = data["next_end_date"]

                remaining_months -= chunk_months

    return all_records, corporate_actions


def calculate_metrics(records):

    start_price = records[0]["close"]
    end_price = records[-1]["close"]

    highest_price = max(
        record["high"]
        for record in records
    )

    lowest_price = min(
        record["low"]
        for record in records
    )

    average_volume = sum(
        record["volume"]
        for record in records
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


def find_volume_spikes(records, multiplier=2):

    average_volume = sum(
        record["volume"]
        for record in records
    ) / len(records)

    spikes = []

    for record in records:

        if record["volume"] >= average_volume * multiplier:

            spikes.append({
                "date": record["date"],
                "volume": record["volume"],
                "close": record["close"],
                "multiple": record["volume"] / average_volume
            })

    return spikes


def find_large_moves(records, threshold=3):

    large_moves = []

    for record in records:

        if record["prevClose"] == 0:
            continue

        change_pct = (
            (record["close"] - record["prevClose"])
            / record["prevClose"]
            * 100
        )

        if abs(change_pct) >= threshold:
