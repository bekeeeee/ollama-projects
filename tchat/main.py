from langchain_community.chat_models import ChatOllama
from langchain import LLMChain
from langchain.prompts import (
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langchain.memory import ConversationBufferMemory, FileChatMessageHistory

chat = ChatOllama(model="llama3")
memory = ConversationBufferMemory(
    # chat_memory=FileChatMessageHistory("chat_history.json"),
    memory_key="messages",
    return_messages=True,
)
prompt = ChatPromptTemplate(
    input_variables=[
        "content",
        "messages",
    ],  # the current user input & past stored messages
    messages=[
        MessagesPlaceholder(variable_name="messages"),
        HumanMessagePromptTemplate.from_template("{content}"),
    ],
)

chain = LLMChain(llm=chat, prompt=prompt, memory=memory)

while True:
    content = input(">> ")
    result = chain.invoke({"content": content})
    print(result["text"])
