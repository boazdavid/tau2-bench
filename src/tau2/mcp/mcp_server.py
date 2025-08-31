import asyncio
import json
from threading import Thread
import time

from fastmcp import FastMCP
from fastmcp.client import Client
from fastmcp.client.transports import StreamableHttpTransport

from tau2.domains.airline.tools import AirlineTools

PORT = 8765
def run_server():
    db = {}
    tools_obj = AirlineTools(db)
    mcp = FastMCP()

    for attr_name in dir(tools_obj):
        if attr_name.startswith("_"):
            continue
        attr = getattr(tools_obj, attr_name)
        if callable(attr) and getattr(attr, "__tool__", None):
            mcp.tool(attr)

    mcp.run(transport="http", host="localhost", port=PORT)

def start_server_in_thread():
    thread = Thread(target=run_server, daemon=True)
    thread.start()
    time.sleep(2)  # give server time to start
    return thread

async def run_client():        
    transport = StreamableHttpTransport(
        url=f"http://127.0.0.1:{PORT}/mcp"        
    )
    async with Client(transport) as client:
        print("Calling list_tools...")
        tools = await client.list_tools()
        print("Available tools:")
        for t in tools:
            print("-", t.name)                        
            print("INPUT SCHEMA:")
            print(json.dumps(t.inputSchema, indent=2))
            print("OUTPUT SCHEMA:")
            print(json.dumps(t.outputSchema, indent=2))
            print("-" * 40)

        result = await client.call_tool(
            "list_all_airports",
            {}            
        )        
        print(result.data)

if __name__ == "__main__":
    # run_server()
    start_server_in_thread()
    asyncio.run(run_client())
