import asyncio
import json

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


NSE_URL = "https://mcp.nseindia.in/bhavcopy/cm/mcp"


# ============================================
# GET STOCK DATA FROM NSE MCP
# ============================================

async def get_stock_history(symbol, months=3, end_date="today"):

    all_records = []
    remaining_months = months
    corporate_actions = {}
    week_52 = None

    async with streamable_http_client(NSE_URL) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            # --------------------------------
            # CORPORATE ACTIONS
            # --------------------------------

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

            # --------------------------------
            # 52 WEEK HIGH / LOW
            # --------------------------------

            result = await session.call_tool(
                "get_52_week_high_low",
                {
                    "symbol": symbol
                }
            )

            if result.is_error:

                print("52-week high/low error:")
                print(result.content)

            else:

                week_52 = json.loads(
                    result.content[0].text
                )

            # --------------------------------
            # HISTORICAL DATA
            # --------------------------------

            while remaining_months > 0:

                chunk_months = min(
                    3,
                    remaining_months
                )

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

                    return None, None, None

                data = json.loads(
                    result.content[0].text
                )

                all_records = (
                    data["data"]
                    + all_records
                )

                end_date = data["next_end_date"]

                remaining_months -= chunk_months

    return (
        all_records,
        corporate_actions,
        week_52
    )


# ============================================
# BASIC METRICS
# ============================================

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


# ============================================
# MOVING AVERAGE
# ============================================

def calculate_moving_average(records, window):

    if len(records) < window:
        return None

    closes = [
        record["close"]
        for record in records
    ]

    recent_closes = closes[-window:]

    return sum(recent_closes) / window


# ============================================
# TREND
# ============================================

def calculate_trend(records):

    current_price = records[-1]["close"]

    ma20 = calculate_moving_average(
        records,
        20
    )

    ma50 = calculate_moving_average(
        records,
        50
    )

    result = {
        "current_price": current_price,
        "ma20": ma20,
        "ma50": ma50
    }

    if ma20 is not None:

        result["price_vs_ma20_pct"] = (
            (current_price - ma20)
            / ma20
            * 100
        )

    else:

        result["price_vs_ma20_pct"] = None

    if ma50 is not None:

        result["price_vs_ma50_pct"] = (
            (current_price - ma50)
            / ma50
            * 100
        )

    else:

        result["price_vs_ma50_pct"] = None

    if ma20 is not None and ma50 is not None:

        result["ma20_above_ma50"] = (
            ma20 > ma50
        )

    else:

        result["ma20_above_ma50"] = None

    return result


# ============================================
# VOLUME SPIKES
# ============================================

def find_volume_spikes(records, multiplier=2):

    average_volume = sum(
        record["volume"]
        for record in records
    ) / len(records)

    spikes = []

    for record in records:

        if record["volume"] >= (
            average_volume * multiplier
        ):

            spikes.append({
                "date": record["date"],
                "volume": record["volume"],
                "close": record["close"],
                "multiple": (
                    record["volume"]
                    / average_volume
                )
            })

    return spikes


# ============================================
# LARGE PRICE MOVES
# ============================================

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


# ============================================
# CORPORATE ACTION MATCHING
# ============================================

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
                    "adjustment_factor": action[
                        "adjustmentFactor"
                    ]
                })

    return matches


# ============================================
# IMPORTANT EVENTS
# ============================================

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
            abs(price_change)
            >= price_threshold
        )

        volume_spike = (
            volume_multiple
            >= volume_multiplier
        )

        corporate_action = None

        for action in actions:

            if record["date"] == action["exDate"]:

                corporate_action = {
                    "action_type": action["actionType"],
                    "purpose": action["purpose"],
                    "adjustment_factor": action[
                        "adjustmentFactor"
                    ]
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


# ============================================
# SUPPORT LEVELS
# ============================================

def find_support_levels(records, tolerance=0.02):

    lows = [
        record["low"]
        for record in records
    ]

    levels = []

    for i in range(2, len(lows) - 2):

        if (
            lows[i] <= lows[i - 1]
            and lows[i] <= lows[i + 1]
            and lows[i] <= lows[i - 2]
            and lows[i] <= lows[i + 2]
        ):

            level = lows[i]

            matched = False

            for existing in levels:

                if (
                    abs(level - existing["level"])
                    / existing["level"]
                    <= tolerance
                ):

                    existing["prices"].append(level)
                    existing["touches"] += 1

                    existing["level"] = (
                        sum(existing["prices"])
                        / len(existing["prices"])
                    )

                    matched = True
                    break

            if not matched:

                levels.append({
                    "level": level,
                    "touches": 1,
                    "prices": [level]
                })

    return sorted(
        [
            {
                "level": level["level"],
                "touches": level["touches"]
            }
            for level in levels
        ],
        key=lambda x: x["level"]
    )


# ============================================
# RESISTANCE LEVELS
# ============================================

def find_resistance_levels(records, tolerance=0.02):

    highs = [
        record["high"]
        for record in records
    ]

    levels = []

    for i in range(2, len(highs) - 2):

        if (
            highs[i] >= highs[i - 1]
            and highs[i] >= highs[i + 1]
            and highs[i] >= highs[i - 2]
            and highs[i] >= highs[i + 2]
        ):

            level = highs[i]

            matched = False

            for existing in levels:

                if (
                    abs(level - existing["level"])
                    / existing["level"]
                    <= tolerance
                ):

                    existing["prices"].append(level)
                    existing["touches"] += 1

                    existing["level"] = (
                        sum(existing["prices"])
                        / len(existing["prices"])
                    )

                    matched = True
                    break

            if not matched:

                levels.append({
                    "level": level,
                    "touches": 1,
                    "prices": [level]
                })

    return sorted(
        [
            {
                "level": level["level"],
                "touches": level["touches"]
            }
            for level in levels
        ],
        key=lambda x: x["level"]
    )


# ============================================
# COMPLETE STOCK ANALYSIS
# ============================================

async def analyze_stock(symbol, months=6):

    (
        records,
        corporate_actions,
        week_52
    ) = await get_stock_history(
        symbol,
        months
    )

    if records is None:
        return None

    # --------------------------------
    # METRICS
    # --------------------------------

    metrics = calculate_metrics(
        records
    )

    # --------------------------------
    # TREND
    # --------------------------------

    trend = calculate_trend(
        records
    )

    # --------------------------------
    # SUPPORT / RESISTANCE
    # --------------------------------

    support_levels = find_support_levels(
        records
    )

    resistance_levels = find_resistance_levels(
        records
    )

    # --------------------------------
    # VOLUME SPIKES
    # --------------------------------

    volume_spikes = find_volume_spikes(
        records
    )

    # --------------------------------
    # LARGE PRICE MOVES
    # --------------------------------

    large_moves = find_large_moves(
        records
    )

    # --------------------------------
    # CORPORATE ACTION MATCHES
    # --------------------------------

    corporate_action_matches = (
        match_corporate_actions(
            large_moves,
            corporate_actions
        )
    )

    # --------------------------------
    # IMPORTANT EVENTS
    # --------------------------------

    important_events = (
        build_important_events(
            records,
            corporate_actions
        )
    )

    # --------------------------------
    # FINAL ANALYSIS OBJECT
    # --------------------------------

    analysis = {

        "symbol": symbol,

        "period": {
            "from": records[0]["date"],
            "to": records[-1]["date"],
            "trading_days": len(records)
        },

        "metrics": metrics,

        "52_week": week_52,

        "trend": trend,

        "support_levels": support_levels,

        "resistance_levels": resistance_levels,

        "volume_spikes": volume_spikes,

        "large_moves": large_moves,

        "corporate_actions": corporate_actions,

        "corporate_action_matches": (
            corporate_action_matches
        ),

        "important_events": important_events
    }

    return analysis


# ============================================
# LLM-READY SUMMARY
# ============================================

def build_llm_summary(analysis):

    summary = {

        "symbol": analysis["symbol"],

        "period": analysis["period"],

        "current_price": analysis[
            "trend"
        ]["current_price"],

        "performance": {

            "return_pct": analysis[
                "metrics"
            ]["return_pct"],

            "max_drawdown_pct": analysis[
                "metrics"
            ]["max_drawdown"],

            "highest_price": analysis[
                "metrics"
            ]["highest_price"],

            "lowest_price": analysis[
                "metrics"
            ]["lowest_price"]
        },

        "52_week": analysis[
            "52_week"
        ],

        "trend": {

            "ma20": analysis[
                "trend"
            ]["ma20"],

            "ma50": analysis[
                "trend"
            ]["ma50"],

            "price_vs_ma20_pct": analysis[
                "trend"
            ]["price_vs_ma20_pct"],

            "price_vs_ma50_pct": analysis[
                "trend"
            ]["price_vs_ma50_pct"],

            "ma20_above_ma50": analysis[
                "trend"
            ]["ma20_above_ma50"]
        },

        "support_levels": analysis[
            "support_levels"
        ],

        "resistance_levels": analysis[
            "resistance_levels"
        ],

        "important_events": analysis[
            "important_events"
        ],

        "corporate_actions": analysis[
            "corporate_actions"
        ]
    }

    return summary


# ============================================
# MAIN
# ============================================

async def main():

    symbol = "CYIENT"

    analysis = await analyze_stock(
        symbol,
        6
    )

    if analysis is None:
        return

    llm_summary = build_llm_summary(
        analysis
    )

    print(
        json.dumps(
            llm_summary,
            indent=2
        )
    )


asyncio.run(main())
