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

            large_moves.append({
                "date": record["date"],
                "close": record["close"],
                "prev_close": record["prevClose"],
                "change_pct": change_pct,
                "volume": record["volume"]
            })

    return large_moves


def match_corporate_actions(
    large_moves,
    corporate_actions
):

    matches = []

    actions = corporate_actions.get(
        "actions",
        []
    )

    for move in large_moves:

        for action in actions:

            if move["date"] == action["exDate"]:

                matches.append({
                    "date": move["date"],
                    "price_change": move["change_pct"],
                    "action_type": action["actionType"],
                    "purpose": action["purpose"],
                    "adjustment_factor": action["adjustmentFactor"]
                })

    return matches


def build_important_events(
    records,
    corporate_actions,
    volume_multiplier=2,
    price_threshold=3
):

    average_volume = sum(
        record["volume"]
        for record in records
    ) / len(records)

    actions = corporate_actions.get(
        "actions",
        []
    )

    events = []

    for record in records:

        price_change = 0

        if record["prevClose"] != 0:

            price_change = (
                (record["close"] - record["prevClose"])
                / record["prevClose"]
                * 100
            )

        volume_multiple = (
            record["volume"]
            / average_volume
        )

        large_price_move = (
            abs(price_change) >= price_threshold
        )

        volume_spike = (
            volume_multiple >= volume_multiplier
        )

        corporate_action = None

        for action in actions:

            if record["date"] == action["exDate"]:

                corporate_action = {
                    "action_type": action["actionType"],
                    "purpose": action["purpose"],
                    "adjustment_factor": action["adjustmentFactor"]
                }

        if (
            large_price_move
            or volume_spike
            or corporate_action is not None
        ):

            events.append({
                "date": record["date"],
                "close": record["close"],
                "price_change_pct": price_change,
                "volume": record["volume"],
                "volume_multiple": volume_multiple,
                "large_price_move": large_price_move,
                "volume_spike": volume_spike,
                "corporate_action": corporate_action
            })

    return events


async def main():

    symbol = "CYIENT"

    records, corporate_actions = await get_stock_history(
        symbol,
        6
    )

    if records is None:
        return

    # --------------------------------
    # METRICS
    # --------------------------------

    metrics = calculate_metrics(records)

    print("\n==============================")
    print("STOCK HISTORY")
    print("==============================")

    print("Symbol:", symbol)
    print("Records:", len(records))
    print("From:", records[0]["date"])
    print("To:", records[-1]["date"])

    print("\n==============================")
    print("METRICS")
    print("==============================")

    print(
        "Start price:",
        metrics["start_price"]
    )

    print(
        "End price:",
        metrics["end_price"]
    )

    print(
        "Return %:",
        round(metrics["return_pct"], 2)
    )

    print(
        "Highest price:",
        metrics["highest_price"]
    )

    print(
        "Lowest price:",
        metrics["lowest_price"]
    )

    print(
        "Average volume:",
        round(metrics["average_volume"])
    )

    print(
        "Max drawdown %:",
        round(metrics["max_drawdown"], 2)
    )

    # --------------------------------
    # VOLUME SPIKES
    # --------------------------------

    spikes = find_volume_spikes(records)

    print("\n==============================")
    print("VOLUME SPIKES")
    print("==============================")

    for spike in spikes:

        print(
            spike["date"],
            "Volume:",
            spike["volume"],
            "Close:",
            spike["close"],
            "Multiple:",
            round(spike["multiple"], 2),
            "x"
        )

    # --------------------------------
    # LARGE PRICE MOVES
    # --------------------------------

    large_moves = find_large_moves(records)

    print("\n==============================")
    print("LARGE PRICE MOVES")
    print("==============================")

    for move in large_moves:

        print(
            move["date"],
            "Change:",
            round(move["change_pct"], 2),
            "%",
            "Close:",
            move["close"],
            "Volume:",
            move["volume"]
        )

    # --------------------------------
    # CORPORATE ACTIONS
    # --------------------------------

    print("\n==============================")
    print("CORPORATE ACTIONS")
    print("==============================")

    print(
        json.dumps(
            corporate_actions,
            indent=2
        )
    )

    # --------------------------------
    # CORPORATE ACTION MATCHES
    # --------------------------------

    matches = match_corporate_actions(
        large_moves,
        corporate_actions
    )

    print("\n==============================")
    print("CORPORATE ACTION MATCHES")
    print("==============================")

    for match in matches:

        print(
            match["date"],
            "Change:",
            round(match["price_change"], 2),
            "%",
            "Action:",
            match["action_type"],
            "Purpose:",
            match["purpose"],
            "Adjustment:",
            match["adjustment_factor"]
        )

    # --------------------------------
    # IMPORTANT EVENTS
    # --------------------------------

    events = build_important_events(
        records,
        corporate_actions
    )

    print("\n==============================")
    print("IMPORTANT EVENTS")
    print("==============================")

    for event in events:

        print(
            event["date"],
            "| Change:",
            round(event["price_change_pct"], 2),
            "%",
            "| Volume:",
            event["volume"],
            "| Volume:",
            round(event["volume_multiple"], 2),
            "x",
            "| Price move:",
            event["large_price_move"],
            "| Volume spike:",
            event["volume_spike"],
            "| Corporate action:",
            event["corporate_action"]
        )


asyncio.run(main())
