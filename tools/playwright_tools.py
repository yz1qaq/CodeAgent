
from utils.mcp import create_mcp_stdio_client


async def get_playwright_tool():
    params = {
        "command": "npx",
       "args": [
        "-y",
        "@executeautomation/playwright-mcp-server"
      ],
    }

    client, tools = await create_mcp_stdio_client("playwright", params)
    return tools