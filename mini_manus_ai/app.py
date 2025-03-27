from http.client import HTTPException
from fastapi import FastAPI
from langgraph_main import mini_manus_main


app = FastAPI()

@app.get("/ask_question")
async def ask_question(question: str, agents_names: str, years_quarters: str):

    try:
        agents = ["final_answer"]
        year = []
        quarter = []

        for agent_name in agents_names:
            if agent_name == 'RAG Agent':
                agent = "rag_search_agent"
                agents.append(agent)
            elif agent_name == 'Snowflake Agent':
                agent = "snowflake_data"
                agents.append(agent)
            elif agent_name == 'Web Search Agent':
                agent = "web_search"
                agents.append(agent)

        for year_quarter in years_quarters:
            year_only, quarter_only = year_quarter.split(" Q")
            year.append(int(year_only))
            quarter.append(int(quarter_only))

        result = mini_manus_main(question, agents, year, quarter)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error returning a response: {str(e)}")
    
    return result