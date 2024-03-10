import json
from dotenv import load_dotenv

load_dotenv()

from langchain.cache import InMemoryCache
from langchain.globals import set_llm_cache
from langchain.memory import ConversationBufferWindowMemory
from langchain.schema.runnable import (
    RunnableBranch,
    RunnableLambda,
    RunnablePassthrough,
)

from chatbot.classify import classify_chain

# from chatbot.extracter import extract_chain
# from chatbot.general import general_chain
from chatbot.get_context import context_chain

set_llm_cache(InMemoryCache())


def call_chat(prompt_input, context):

    print("Prompt Input:")
    print(prompt_input)
    print("Context:")
    print(context)

    out = {
        "extract": None,
        "quick_add": None,
        "classification": None,
        "general": None,
    }

    try:
        # print("-" * 50)

        # Chat Memory

        memory = ConversationBufferWindowMemory(k=10, memory_key="history")

        i = 1
        while i < len(context):
            conversation = []
            for j in range(i, len(context)):
                message = context[j]
                if message["user"] == "user":
                    conversation.append({"input": message["message"]})
                elif message["user"] == "agent":
                    conversation.append({"output": message["message"]})
                    i = j + 1
                    break
            memory.save_context(*conversation)

        print("Chat Memory:")
        print(memory.chat_memory)

        # Scheduler

        llm = (
            {
                "context": context_chain,
                "input": lambda x: x["input"],
            }
            | RunnablePassthrough.assign(classification=classify_chain)
            # | RunnableBranch(
            #     (
            #         lambda x: x["classification"] == "yes",
            #         RunnablePassthrough.assign(extract=extract_chain),
            #     ),
            #     RunnablePassthrough.assign(general=general_chain),
            # )
        )

        # Output

        llm_output = llm.invoke(
            {"input": prompt_input.strip(), "history": str(memory.chat_memory)}
        )

    #     print("Scheduler Output:")
    #     print(json.dumps(llm_output, indent=4))

    #     # print("-" * 50)

    except Exception as e:
        print(e)
        return {**out, "error": str(e)}

    return {**out, **llm_output}
