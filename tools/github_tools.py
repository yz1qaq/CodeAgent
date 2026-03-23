import os
from utils.mcp import create_mcp_stdio_client


async def get_github_tool():
    # 不要写死 token，优先从环境变量读取
    token = os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN")
    if not token:
        raise ValueError("请先设置 GITHUB_PERSONAL_ACCESS_TOKEN 环境变量")

    params = {
        "command": "npx",
        "args": [
            "-y",
            "@modelcontextprotocol/server-github"
        ],
        "env": {
            **os.environ,  # 继承当前环境
            "GITHUB_PERSONAL_ACCESS_TOKEN": token
        }
    }

    client, tools = await create_mcp_stdio_client("github", params)
    return tools