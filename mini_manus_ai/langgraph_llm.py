import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from final_answer_la import final_answer
from snowflake_la import snowflake_data
from rag_la import rag_search_filter
from web_search_la import web_search
from langchain_core.agents import AgentAction


load_dotenv(r'C:\Users\Admin\Desktop\MS Data Architecture and Management\DAMG 7245 - Big Data Systems and Intelligence Analytics\Assignment 5 A\environment\access.env')


system_prompt = """You are Mini Manus, the great AI research assistant.
Given the user's query you must write a research report with it based on the
list of tools provided to you.

The input query has a list of tools. You are allowed to use only the tools mentioned 
in the input query. Do NOT use any other tools that are not mentioned in the input query.
If you see that a tool has been used (in the scratchpad) with a particular
query, do NOT use that same tool with the same query again. Also, do NOT use
any tool more than twice (ie, if the tool appears in the scratchpad twice, do
not use it again).

Pinecone database has NVIDIA quarterly reports.
Use the metadata filtering to search for information based on years and quarters in Pincone database.
Snowflake database has the quarterly statistics (Valuation Measures) for NVIDIA Corporation.
You can also web search any information related to the given query. You must provide all the links 
to the websites.

You should aim to collect information from a diverse range of sources before
providing the answer to the user. You must not make up any information.
Once you have collected plenty of information to answer the user's question 
(stored in the scratchpad) use the final_answer tool."""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    ("assistant", "scratchpad: {scratchpad}"),
])


llm = ChatOpenAI(
    model="gpt-4o",
    openai_api_key=os.environ["OPENAI_API_KEY"],
    temperature=0
)


tools=[
    rag_search_filter,
    snowflake_data,
    web_search,
    final_answer
]

# define a function to transform intermediate_steps from list
# of AgentAction to scratchpad string
def create_scratchpad(intermediate_steps: list[AgentAction]):
    research_steps = []
    for i, action in enumerate(intermediate_steps):
        if action.log != "TBD":
            # this was the ToolExecution
            research_steps.append(
                f"Tool: {action.tool}, input: {action.tool_input}\n"
                f"Output: {action.log}"
            )
    return "\n---\n".join(research_steps)


mini_manus = (
    {
        "input": lambda x: x["input"],
        "chat_history": lambda x: x["chat_history"],
        "scratchpad": lambda x: create_scratchpad(
            intermediate_steps=x["intermediate_steps"]
        ),
    }
    | prompt
    | llm.bind_tools(tools, tool_choice="any")
)



def run_mini_manus(state: list):
    print("run_mini_manus")
    print(f"intermediate_steps: {state['intermediate_steps']}")
    out = mini_manus.invoke(state)
    tool_name = out.tool_calls[0]["name"]
    tool_args = out.tool_calls[0]["args"]
    action_out = AgentAction(
        tool=tool_name,
        tool_input=tool_args,
        log="TBD"
    )
    return {
        "intermediate_steps": [action_out]
    }


def router(state: list):
    # return the tool name to use
    if isinstance(state["intermediate_steps"], list):
        return state["intermediate_steps"][-1].tool
    else:
        # if we output bad format go to final answer
        print("Router invalid format")
        return "final_answer"



# Test
#inputs = {
#    "input": "tell me something interesting about dogs",
#    "chat_history": [],
#    "intermediate_steps": [],
#}

#out = mini_manus.invoke(inputs)

#print(out.tool_calls[0]["name"])
#print(out.tool_calls[0]["args"])
