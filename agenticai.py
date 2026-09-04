"""
01 - TOOL CALLING (Ollama)
--------------------------
Shows the core idea: the LLM DECIDES to call a function,
our Python code ACTUALLY runs it, then we send the result back.

Run:
    python 01_tool_calling.py
"""

from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage


# 1. Define normal Python functions as "tools"
@tool
def get_weather(city: str) -> str:
    """Get the current weather for a given city."""
    # Fake weather data just for the demo (no API key needed)
    fake_data = {
        "mumbai": "32°C, humid, chance of rain",
        "delhi": "38°C, sunny",
        "bangalore": "24°C, pleasant",
    }
    return fake_data.get(city.lower(), "Weather data not available for this city.")


@tool
def add_numbers(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b


tools = [get_weather, add_numbers]

# 2. Load a local, free model via Ollama and attach the tools
llm = ChatOllama(model="llama3.2", temperature=0)
llm_with_tools = llm.bind_tools(tools)

# 3. Ask a question that needs a tool
question = "What's the weather in Mumbai, and what is 45 + 78?"
messages = [HumanMessage(content=question)]

response = llm_with_tools.invoke(messages)
print("\nModel wants to call these tools:")
print(response.tool_calls)

messages.append(response)

# 4. WE run the actual tool (the model never runs code itself)
tool_lookup = {t.name: t for t in tools}
for call in response.tool_calls:
    tool_fn = tool_lookup[call["name"]]
    result = tool_fn.invoke(call["args"])
    print(f"\nRan tool '{call['name']}' with args {call['args']} -> {result}")

    # send the tool's result back to the model
    from langchain_core.messages import ToolMessage
    messages.append(ToolMessage(content=str(result), tool_call_id=call["id"]))

# 5. Ask the model to give the final answer using the tool results
final = llm_with_tools.invoke(messages)
print("\nFINAL ANSWER:\n", final.content)