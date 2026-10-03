import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

NSE_URL = "https://mcp.nseindia.in/bhavcopy/cm/mcp"


async def main():

    async with streamable_http_client(NSE_URL) as (read, write, _):

        async with ClientSession(read, write) as session:

            await session.initialize()

            tools = await session.list_tools()

            print("\nAvailable NSE tools:\n")

            for tool in tools.tools:
                print("-", tool.name)
                print(" ", tool.description)


asyncio.run(main())
