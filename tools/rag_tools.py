from utils.mcp import create_mcp_stdio_client
async def get_stdio_rag_tools():
    params = {
        "command":"python",
        "args":[
            "/Users/yz1/Learn/Code_Agent/m_mcp/rag_tools.py"
        ]
    }

    client,tools = await create_mcp_stdio_client("rag_tools",params)

    return tools



if __name__== "__main__":
    print("tools.rag_tools.py!")
