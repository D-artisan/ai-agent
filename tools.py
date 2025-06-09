from langchain_community.tools import DuckDuckGoSearchRun
from datetime import datetime

# Minimal Tool class for compatibility
class Tool:
    def __init__(self, name, func, description=None):
        self.name = name
        self.func = func
        self.description = description

def save_to_txt(data: str, filename: str = "research_output.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"
    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)
    return f"Data successfully saved to {filename}"

save_tool = Tool(
    name="save_text_to_file",
    func=save_to_txt,
    description="Saves structured research data to a text file.",
)

search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="search",
    func=search.run,
    description="Search the web for information",
)

import wikipedia
def wikipedia_lookup(query):
    try:
        return wikipedia.summary(query, sentences=3)
    except Exception as e:
        return f"Wikipedia lookup error: {e}"
wiki_tool = Tool(
    name="wiki",
    func=wikipedia_lookup,
    description="Search Wikipedia for information.",
)