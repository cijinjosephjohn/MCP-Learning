from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq


from dotenv import load_dotenv
load_dotenv()

import asyncio
import os

async def main():
    client = MultiServerMCPClient(
        {
            "math":{
                "command":"python",
                "args":["mathserver.py"], ##Absolute path
                "transport":"stdio"
            },
            "weather":{
                "url":"http://127.0.0.1:8000/mcp",
                "transport": "streamable_http"
            }
        }
    )
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
    tools = await client.get_tools()
    model = ChatGroq(model="llama-3.1-8b-instant")
    agent = create_react_agent(
        model,tools
    )


    # math_response = await agent.ainvoke(
    #     {"messages": [{"role": "user", "content": "what's (5+3)x12?"}]}
    # )
    # print("Math response:", math_response['messages'][-1].content)
    weather_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "What is the weather in California ?"}]}
    )

    print("Weather response:", weather_response['messages'][-1].content)


asyncio.run(main())


