from langgraph.checkpoint import mongodb
from model.model import qwen_llm

from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.redis import RedisSaver
from langchain.agents import create_agent
from langgraph.checkpoint.mongodb import MongoDBSaver
from tools.file_tools import file_tools


def pretty_print(res):
    messages = res.get("messages", [])
    
    for msg in messages:
        role = msg.type  # human / ai / tool
        
        if role == "human":
            print(f"User: {msg.content}")
        elif role == "ai":
            print(f"Assistant: {msg.content}")
        elif role == "tool":
            print(f"[Tool]: {msg.content}")
    
    print("=" * 60)


def run_agent():
    with RedisSaver.from_conn_string("redis://localhost:6379") as memory:
        memory.setup()


        qwen_agent = create_agent(
            model=qwen_llm,
            tools=file_tools,
            checkpointer=memory,
            debug=False   # 建议先关掉，不然太吵
        )

        config = RunnableConfig(configurable={"thread_id": "3"})

        print("====== Round 1 ======")
        res1 = qwen_agent.invoke(
            input={
                "messages": [
                    {"role": "user", "content": "你好，我是yz1"}
                ]
            },
            config=config
        )
        pretty_print(res1)

        print("====== Round 2 ======")
        res2 = qwen_agent.invoke(
            input={
                "messages": [
                    {"role": "user", "content": "我是谁?你只需要说出我的名字"}
                ]
            },
            config=config
        )
        pretty_print(res2)
      



if __name__ == "__main__":
    run_agent()