async def main():

    all_records = []

    end_date = "2026-10-01"

    for i in range(2):

        data = await get_stock_history(
            "CYIENT",
            3,
            end_date
        )

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
