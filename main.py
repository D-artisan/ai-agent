import os
from env import load_env
from pydantic import BaseModel, ValidationError
from litellm import completion
from tools import search_tool, wiki_tool, save_tool

load_env()

def get_completion(prompt, model="openrouter/microsoft/mai-ds-r1:free"):
    try:
        response = completion(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            api_base="https://openrouter.ai/api/v1",
            max_tokens=1000,
            temperature=0.0,
            headers={
                "HTTP-Referer": "http://localhost:5000",
                "X-Title": "AI Agent Tutorial",
                "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}"
            }
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

SYSTEM_PROMPT = '''
You are a research assistant that will help generate a research paper.
You have access to these tools: search (web search), wiki (Wikipedia lookup), save_text_to_file (save research to a text file).
When answering, use the tools as needed and always list the tools you used in the 'tools_used' field, even if you only considered them.
If you use a tool, specify it in 'tools_used' as 'tool_name: argument'.
Always return a valid JSON object with ALL of these fields: topic (str), summary (str), sources (list of str), tools_used (list of str).
If you do not use a tool, return an empty list for tools_used. If you do not have sources, return an empty list for sources.
Wrap the output in this format and provide no other text:
{{format_instructions}}
'''

FORMAT_INSTRUCTIONS = '{"topic": string, "summary": string, "sources": list of string, "tools_used": list of string}'

def build_prompt(user_query, tool_descriptions):
    return SYSTEM_PROMPT.replace("{format_instructions}", FORMAT_INSTRUCTIONS) + f"\n\nAvailable tools:\n{tool_descriptions}\n\nUser query: {user_query}"

tools = {
    "search": search_tool.func,
    "wiki": wiki_tool.func,
    "save_text_to_file": save_tool.func,
}

if __name__ == "__main__":
    user_query = input("What can I help you research? ")
    tool_descriptions = "".join([
        f"- {search_tool.name}: {search_tool.description}\n",
        f"- {wiki_tool.name}: {wiki_tool.description}\n",
        f"- {save_tool.name}: {save_tool.description}\n"
    ])
    prompt = build_prompt(user_query, tool_descriptions)
    llm_response = get_completion(prompt)
    print("\nRaw LLM Response:\n", llm_response)
    if not llm_response or not llm_response.strip():
        print("LLM returned an empty response. Please try again or check your API/model settings.")
    else:
        try:
            import json
            parsed = ResearchResponse.model_validate(json.loads(llm_response))
            print("\nParsed Response:")
            print(parsed)
            print("\nAgent process:")
            for tool in parsed.tools_used:
                tool_name = tool.split(':')[0].strip().lower()
                arg = tool.split(':', 1)[1].strip() if ':' in tool else user_query
                print(f"Agent decided to use tool: {tool_name} with argument: {arg}")
                if tool_name in tools:
                    print(f"Calling tool '{tool_name}'...")
                    result = tools[tool_name](arg)
                    print(f"Tool '{tool_name}' result: {result}")
                else:
                    print(f"Tool '{tool_name}' not found.")
            print("Saving summary to file using save_text_to_file...")
            save_result = tools["save_text_to_file"](parsed.summary)
            print(f"Tool 'save_text_to_file' result: {save_result}")
        except Exception as ve:
            print("Could not parse response, trying to fix...", ve)
            import json
            try:
                data = json.loads(llm_response)
                if "sources" not in data:
                    data["sources"] = []
                if "tools_used" not in data:
                    data["tools_used"] = []
                parsed = ResearchResponse.model_validate(data)
                print("\nParsed Response (after fix):")
                print(parsed)
                for tool in parsed.tools_used:
                    tool_name = tool.split(':')[0].strip().lower()
                    arg = tool.split(':', 1)[1].strip() if ':' in tool else user_query
                    if tool_name in tools:
                        result = tools[tool_name](arg)
                        print(f"Tool '{tool_name}' result: {result}")
            except Exception as ve2:
                print("Still could not parse response:", ve2)

