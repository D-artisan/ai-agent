# AI Agent Tutorial

This project demonstrates a research assistant agent that can:
- Search the web using DuckDuckGo
- Look up information on Wikipedia
- Save research summaries to a text file
- Use an LLM (via OpenRouter) to generate structured research responses

## Features
- **Tool-calling**: The agent can call real tools (search, wiki, save) based on LLM output.
- **Structured output**: Uses Pydantic for robust parsing of LLM responses.
- **Verbose agent process**: See step-by-step reasoning and tool usage in the terminal.
- **Safe by default**: `.env` and `research_output.txt` are git-ignored.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Add your OpenRouter API key to `.env`:
   ```env
   OPENROUTER_API_KEY=your-key-here
   ```

## Usage
Run the agent:
```bash
python main.py
```
Enter your research question when prompted. The agent will:
- Generate a structured response
- Call tools as needed (search, wiki, save)
- Save the summary to `research_output.txt`

## Project Structure
- `main.py` — Main agent logic and tool-calling
- `tools.py` — Real tool implementations (search, wiki, save)
- `env.py` — Loads environment variables
- `requirements.txt` — Python dependencies
- `.gitignore` — Excludes sensitive/generated files from git

## Notes
- The agent expects the LLM to return a JSON object with `topic`, `summary`, `sources`, and `tools_used` fields.
- If the LLM omits fields, the code will attempt to fix the output.
- All research summaries are saved to `research_output.txt` by default.

---
MIT License
