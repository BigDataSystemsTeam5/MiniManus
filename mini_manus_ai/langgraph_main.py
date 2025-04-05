from langgraph.graph import StateGraph, END
from agentstate_la import AgentState
from langgraph_llm import router, run_mini_manus
from snowflake_la import snowflake_data
from report_builder import build_report
from tool_runner import run_tool
from rag_la import rag_search_filter
from web_search_la import web_search
from final_answer_la import final_answer
from IPython.display import Image



def mini_manus_main(question, agents, years_quarters):
    graph = StateGraph(AgentState)

    graph.add_node("mini_manus", run_mini_manus)
    graph.add_node("rag_search_filter", run_tool)
    graph.add_node("snowflake_data", run_tool)
    graph.add_node("web_search", run_tool)
    graph.add_node("final_answer", run_tool)

    graph.set_entry_point("mini_manus")

    graph.add_conditional_edges(
        source="mini_manus",  # where in graph to start
        path=router,  # function to determine which node is called
    )

    tools=[
        snowflake_data,
        rag_search_filter,
        web_search,
        final_answer
    ]


    # create edges from each tool back to the mini_manus
    for tool_obj in tools:
        if tool_obj.name != "final_answer":
            graph.add_edge(tool_obj.name, "mini_manus")

    # if anything goes to final answer, it must then move to END
    graph.add_edge("final_answer", END)

    runnable = graph.compile()

    #Image(runnable.get_graph().draw_png())

    out = runnable.invoke({
        "input": f"""A string list of years and quarters is provided: {years_quarters}. The year and quarter is
        separated by a space ( ). The year is mentioned before the space. There is an alphabet Q after space 
        indicatng quarter. The quarter is mentioned after this alphabet Q. Give response to the 
        question: {question} about NVIDIA. The response should be related solely to the information of the 
        years and quarters provided. A string list of tools is provided: {agents}. You are allowed to use the 
        tools mentioned in this list. Do NOT use any other tools. The mentioned tools should be used to get 
        information for all the years and quarters mentioned in the years and quarters lists.""",
        "chat_history": [],
    })

    result = build_report(
        output=out["intermediate_steps"][-1].tool_input
    )

    return result


# Test

#question = "tell me something in short"
#years = [2024]
#quarters = [3, 4]
#agents = ["rag_search_filter"]
#
#result = mini_manus_main(question, agents, years, quarters)
#print(result)