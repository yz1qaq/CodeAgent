from model.model import qwen_llm

from langchain_core.runnables import RunnableConfig
from langchain.agents import create_agent
from langgraph.checkpoint.mongodb import MongoDBSaver
from tools.file_tools import file_tools


def pretty_print(res):
    messages = res.get("messages", [])
    for msg in reversed(messages):
        if msg.type == "ai":
            print(f"Assistant: {msg.content}")
        if msg.type == "tool":
            print(f"tool:{msg.content}")
        print("=" * 60)
        return


def run_agent():
    with MongoDBSaver.from_conn_string("mongodb://localhost:27017", "docker") as memory:
        qwen_agent = create_agent(
            model=qwen_llm,
            tools=file_tools,
            checkpointer=memory,
            debug=False,  # 建议先关掉，不然太吵
        )

        config = RunnableConfig(configurable={"thread_id": "3"})

        while True:
            question = input("用户:")
            if question == "exit":
                break
            res1 = qwen_agent.invoke(
                input={"messages": [{"role": "user", "content": question}]},
                config=config,
            )
            pretty_print(res1)

        memory.close()


if __name__ == "__main__":
    run_agent()
