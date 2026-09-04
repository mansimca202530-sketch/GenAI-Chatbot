"""
04 - AGENTIC AI BIRTHDAY WISHER (Ollama)
----------------------------------------

The agent checks friends' birthdays and generates
personalized birthday wishes automatically.

Run:
    python birthday_agent.py
"""

from datetime import datetime

from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage


# =========================================================
# 1. FRIENDS DATABASE
# =========================================================

friends = {
    "Rahul": {
        "birthday": "09-04",
        "relation": "college friend",
        "style": "funny"
    },

    "Aman": {
        "birthday": "12-15",
        "relation": "best friend",
        "style": "emotional"
    },

    "Sara": {
        "birthday": "03-20",
        "relation": "close friend",
        "style": "friendly"
    }
}


# =========================================================
# 2. TOOL - CHECK BIRTHDAYS
# =========================================================

@tool
def check_birthdays(date: str) -> str:
    """
    Check which friends have their birthday
    on the given date.

    Date format: MM-DD
    """

    birthday_friends = []

    for name, details in friends.items():

        if details["birthday"] == date:

            birthday_friends.append({
                "name": name,
                "relation": details["relation"],
                "style": details["style"]
            })

    if not birthday_friends:
        return "No birthdays today."

    return str(birthday_friends)


# =========================================================
# 3. TOOL - CREATE BIRTHDAY MESSAGE
# =========================================================

@tool
def create_birthday_message(
    name: str,
    relation: str,
    style: str
) -> str:
    """
    Create a birthday message for a friend.
    """

    return (
        f"Create a birthday wish for {name}. "
        f"They are my {relation}. "
        f"Use a {style} style. "
        f"Keep it friendly and suitable for WhatsApp."
    )


# =========================================================
# 4. TOOL - SEND MESSAGE
# =========================================================

@tool
def send_birthday_message(name: str, message: str) -> str:
    """
    Simulate sending a birthday message.

    In this demo the message is only printed.
    """

    print("\n--------------------------------")
    print(f"Message sent to {name}:")
    print(message)
    print("--------------------------------")

    return f"Birthday message sent successfully to {name}."


# =========================================================
# 5. CREATE TOOL LIST
# =========================================================

tools = [
    check_birthdays,
    create_birthday_message,
    send_birthday_message
]


# =========================================================
# 6. LOAD OLLAMA MODEL
# =========================================================

llm = ChatOllama(
    model="llama3.2",
    temperature=0.7
)

llm_with_tools = llm.bind_tools(tools)


# =========================================================
# 7. GET TODAY'S DATE
# =========================================================

today = datetime.now().strftime("%m-%d")

print("Today's date:", today)


# =========================================================
# 8. ASK THE AGENT WHAT TO DO
# =========================================================

question = f"""
Today is {today}.

Check my friends' birthdays.

If someone has a birthday today:
1. Find their details.
2. Create a personalized birthday wish.
3. Send the birthday wish.

If nobody has a birthday today, tell me that there are
no birthdays today.
"""

messages = [
    HumanMessage(content=question)
]


# =========================================================
# 9. FIRST LLM CALL
# =========================================================

response = llm_with_tools.invoke(messages)

print("\nMODEL TOOL CALLS:")
print(response.tool_calls)

messages.append(response)


# =========================================================
# 10. EXECUTE TOOLS
# =========================================================

tool_lookup = {
    t.name: t
    for t in tools
}


for call in response.tool_calls:

    tool_fn = tool_lookup[call["name"]]

    result = tool_fn.invoke(call["args"])

    print(
        f"\nRan tool '{call['name']}' "
        f"with args {call['args']}"
    )

    print("Result:", result)

    messages.append(
        ToolMessage(
            content=str(result),
            tool_call_id=call["id"]
        )
    )


# =========================================================
# 11. FINAL RESPONSE
# =========================================================

final = llm_with_tools.invoke(messages)

print("\nFINAL ANSWER:")
print(final.content)