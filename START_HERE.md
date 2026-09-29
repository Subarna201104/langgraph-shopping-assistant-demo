# Your step-by-step learning path

You do **not** need to understand every file at once. Follow these checkpoints in order.

## 1. Run the app without an API key

Use the three PowerShell commands under **Start here on Windows** in `README.md`. Open the browser page. Leave the mode on **Demo**.

Ask: **What is the price of Nova headphones?** You should see **₹2,499**. The answer comes from a small list in `shop_data.py`. Try **Where is order ORD1001?**; it should say **shipped**. These are fictional records.

Then ask **Summarize our chat**. This first mode is a rules-based practice run. It is not calling an AI model.

## 2. Understand the four basic ideas

- **Message**: what you type, or what the assistant replies.
- **State**: the saved conversation and the chosen route.
- **Node**: one job in the graph, such as looking up an order.
- **Edge**: the path from one job to the next.

In `bot.py`, start reading from `build_graph`. The path is:

```text
Your message → router → products / orders / summary / general → reply
```

Try two questions in the **same chat**: “What is the price of Nova headphones?” and “What about its warranty?” The second question uses the earlier message. `InMemorySaver` keeps the state for your chat's `thread_id` while the app is running.

## 3. See the first *real* AI agent

After you set up your own API key using the README, run `first_agent.py`. It asks the model about three ₹899 mice. The model can call `calculate_total`, which returns **2697**. You will see the tool call, tool result, and final answer printed in PowerShell.

**ReAct in simple words:** the model decides that it needs a tool, uses the tool, reads the result, and then answers. The tool performs the multiplication; the model explains it.

## 4. Turn the full chatbot into AI mode

In the app's sidebar choose **AI**. This changes three things:

1. A model chooses the route from your question and recent conversation.
2. The product and order specialists can call `search_products` or `get_order_status`.
3. For a summary, one model call writes a draft and a second call checks it against the chat.

Try these, one at a time:

1. `What is the warranty on the Orbit keyboard?` → **2 years**.
2. `Where is ORD1002?` → **processing**.
3. `Summarize our chat.` → a short reviewed recap.

If it gives a bad answer, look at the matching tool in `shop_data.py` and the matching instruction inside `bot.py`. This is how you learn to debug a small agent.

## 5. One-minute speaking script

“I made a sample shopping support chatbot with Python and LangGraph. It routes each user message to a product agent, an order agent, a summarizer, or a general response. The product and order agents use tools to read sample data. LangGraph stores the messages for follow-up questions. The summary agent writes a draft and reviews it. I added a no-key demo so I can test the graph before connecting a paid model API.”

## Common problems

- **`py` not found:** install Python with the Windows launcher or use `python` instead.
- **Module not found:** make sure the install command finished, then use `.\.venv\Scripts\python.exe` for every command.
- **API key warning:** Demo works immediately; AI mode needs your own key in `.env` and a restart.
- **Quota or billing error:** check your API account's billing and limits. ChatGPT Plus and the API are billed separately.
- **Wrong sample order:** only `ORD1001`, `ORD1002`, and `ORD1003` exist in this practice data.

