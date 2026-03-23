
from langchain_core.messages import AIMessage, ToolMessage
from model.model import qwen_llm

from langchain_core.runnables import RunnableConfig
from langchain.agents import create_agent
from langgraph.checkpoint.mongodb import MongoDBSaver
from tools.file_tools import file_tools
from tools.cli_tools import get_stdio_cli_tools
import asyncio
from tools.terminal_tools import get_stdio_terminal_tools
from rag.m_rag import retrieve_rag
from tools.github_tools import get_github_tool
from tools.rag_tools import get_stdio_rag_tools
from tools.playwright_tools import get_playwright_tool


def format_debug_output(step_name: str, content: str, is_tool_call=False) -> None:
    if is_tool_call:
        print(f"🔧{step_name}")
    else:
        print(f"🤔{step_name}")
    print("-" * 60)
    print(content.strip())
    print("-" * 60)


async def run_agent():
    with MongoDBSaver.from_conn_string("mongodb://localhost:27017", "docker") as memory:
        cli_tools = await get_stdio_cli_tools()
        rag_tools = await get_stdio_rag_tools()
        ter_tools = await get_stdio_terminal_tools()
        github_tools = await get_github_tool()
        #playwright_tools = await get_playwright_tool()
        
        all_tools = file_tools + ter_tools + cli_tools + github_tools + rag_tools 

        prompt = """你是一位计算机技术专家，你的名字叫moss"
                    
        """
        qwen_agent = create_agent(
            model=qwen_llm,
            tools=all_tools,
            checkpointer=memory,
            debug=False,
            system_prompt=prompt,
        )
        thread_id = 16
        config = RunnableConfig(configurable={"thread_id": thread_id})

        while True:
            question = input("用户问题:")
            if question == "exit":
                break

            print("\n🤖助手正在思考中...")
            print("=" * 60)
            iter_count = 0

            rag_data = retrieve_rag(question)
            if rag_data:
                rag_data = f"""
                  ------------要求-------------------
                    执行任务之前，先考虑是否需要使用retrieve_rag工具检索知识库
                    如果需要，先调用retrieve_rag工具检索知识库，再根据知识库知识执行任务
                    如果不需要，直接执行任务
                --------------------------------------------
                知识库知识:\n{rag_data}\n
                ---------问题-------------\n"""
            else:
                rag_data = ""
            async for chunk in qwen_agent.astream(
                input={"messages": [{"role": "user", "content": rag_data + question}]},
                config=config,
            ):
                iter_count += 1
                print(f"\n iter:{iter_count}")
                print("-" * 60)

                items = chunk.items()
                for node_name, node_output in items:
                    if "messages" in node_output:
                        for msg in node_output["messages"]:
                            if isinstance(msg, AIMessage):
                                if msg.content:
                                    format_debug_output("AI思考", msg.content)
                                else:
                                    for tool in msg.tool_calls:
                                        format_debug_output(
                                            "工具调用", f"{tool['name']}:{tool['args']}"
                                        )

                            elif isinstance(msg, ToolMessage):
                                tool_name = getattr(msg, "name", "unknown")
                                tool_content = msg.content
                                format_debug_output(
                                    "工具执行结果",
                                    f"{tool_name}: {tool_content}",
                                    is_tool_call=True,
                                )

        # memory.close()


if __name__ == "__main__":
    asyncio.run(run_agent())
