import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from tavily import TavilyClient

load_dotenv()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY"),
)
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


# 1. Define the Tool
def web_search(query: str) -> str:
    """Searches the web for recent information."""
    results = tavily.search(query=query, max_results=3)
    return "\n\n".join(
        [
            f"Title: {r['title']}\nSnippet: {r['content']}"
            for r in results.get("results", [])
        ]
    )


# 2. Tool Schema for Function Calling
tools = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the live web for facts or recent news.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query"}
                },
                "required": ["query"],
            },
        },
    }
]

available_tools = {"web_search": web_search}


# 3. Agent Execution Loop
def run_agent(user_goal: str, max_steps: int = 5):
    messages = [
        {
            "role": "system",
            "content": (
                "You are an autonomous research agent. Use the web_search tool "
                "to answer questions with fresh facts. Once you have enough context, "
                "provide a final, synthesized summary."
            ),
        },
        {"role": "user", "content": user_goal},
    ]

    for step in range(max_steps):
        print(f"\n--- Step {step + 1} ---")
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",  # Uses the active model available on your Groq key
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )
        msg = response.choices[0].message

        # If no tool calls, the agent has finished reasoning
        if not msg.tool_calls:
            print("[Agent finished reasoning]")
            return msg.content

        # Append assistant tool call request to the message history
        messages.append({
            "role": "assistant",
            "content": msg.content or "",
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments,
                    },
                }
                for tc in msg.tool_calls
            ],
        })

        # Execute each tool requested
        for tool_call in msg.tool_calls:
            fn_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            print(f"Action: Calling {fn_name}({args})")

            tool_result = available_tools[fn_name](**args)

            # Send the tool result back
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(tool_result),
            })

    return "Agent reached maximum step limit before finishing."


if __name__ == "__main__":
    query = "What is the color of apple?"
    summary = run_agent(query)
    print("\n=== Final Answer ===\n", summary)