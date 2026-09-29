# Build an AI shopping assistant with LangGraph

This is an **original practice project** for the ideas in LinkedIn Learning's *Build AI Agents and Chatbots with LangGraph*. The shop, products, and orders are fictional. It is not a copy of the course's exercise files or a real order system.

If you want to work through the video notebooks exactly, the course's [official exercise repository](https://github.com/LinkedInLearning/build-ai-agents-and-chatbots-with-langgraph-2021112) is separate from this project.

## What you will build

One chatbot can answer product questions, look up sample orders, and summarize your chat. LangGraph sends each message to the right part of the program and remembers the conversation during the current app session.

| Course idea | File to explore | What happens |
| --- | --- | --- |
| Basic ReAct agent and a function tool | `first_agent.py` | Agent uses a multiplication tool |
| Product Q&A and retrieval | `shop_data.py`, `bot.py` | Searches a tiny local catalog |
| Custom orders graph | `bot.py` | Routes order questions to order lookup |
| Reflection | `bot.py` | AI drafts, then reviews a chat summary |
| Multi-agent routing and memory | `bot.py`, `app.py` | Router selects specialist; thread remembers chat |

**Demo mode** works without a model key. It uses rules and sample data so you can learn the graph and test the UI. **AI mode** makes real model calls and can choose tools. API usage can cost money and is billed separately from ChatGPT subscriptions.

## Start here on Windows (PowerShell)

1. Install Python **3.11 or 3.12** from [python.org](https://www.python.org/downloads/) if needed. Open PowerShell in this extracted folder. Check `py --version`.
2. Make a private Python environment and install the packages:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

3. Start the web app:

   ```powershell
   .\.venv\Scripts\python.exe -m streamlit run app.py
   ```

4. In the browser, select **Demo (no key needed)**. Ask: `What is the price of Nova headphones?`, then `What about its warranty?`, then `Where is order ORD1001?`, then `Summarize our chat`.

If `py` is not recognized, install Python with the launcher or use `python` in the same commands. The app opens at `http://localhost:8501` by default. Stop it with **Ctrl+C** in PowerShell.

## Turn on the real AI agents (optional)

1. Get your own OpenAI Platform API key from [API keys](https://platform.openai.com/api-keys) and check [API billing](https://platform.openai.com/settings/organization/billing/overview). A ChatGPT subscription does not include API usage.
2. In PowerShell, run `Copy-Item .env.example .env`, then `notepad .env`. Put your key after `OPENAI_API_KEY=`. Keep `.env` private; never paste the key into a chat, screenshot, or GitHub repository.
3. Restart the web app. Select **AI (API key needed)**. Ask the same four questions.
4. To see a tiny agent use a calculator tool, run:

   ```powershell
   .\.venv\Scripts\python.exe first_agent.py
   ```

The model defaults to `gpt-5-nano`; you can change `MODEL_NAME` in `.env` if your API account supports another tool-calling model.

## See that the graph works

Run the offline checks (they make no API calls):

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## File map

- `app.py`: browser chat screen.
- `bot.py`: LangGraph nodes, routes, memory, and two AI specialist agents.
- `shop_data.py`: fictional catalog and order lookup tools.
- `first_agent.py`: small first exercise with a calculator tool.
- `START_HERE.md`: a slow, step-by-step learning path and plain-English explanations.
- `.env.example`: sample configuration. Your real `.env` is ignored by Git.

InMemorySaver holds conversations only while the app process runs. Restarting the app loses that chat history. Product and order answers are deliberately based on fixed sample records.
