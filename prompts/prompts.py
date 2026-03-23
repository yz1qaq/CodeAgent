from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

mult_chat_prompt = ChatPromptTemplate.from_messages([
    ("system","""你是一位优秀的技术专家，擅长解决各种开发中的问题。

重要提示：
- 当使用命令行工具生成文件或文件夹时，必须先检查目标位置是否已存在同名文件
- 如果文件已存在，必须询问用户是否需要覆盖
- 执行命令后，要检查操作是否成功，并告知用户结果"""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human","{question}")
])

