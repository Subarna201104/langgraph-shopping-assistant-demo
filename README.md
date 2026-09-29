# Shopping Assistant Demo

This is a small practice chatbot that runs in your web browser. It answers questions about a **made-up shop**. The products and orders are examples, so it cannot check a real order or sell anything.

This is an original practice project inspired by LinkedIn Learning's *Build AI Agents and Chatbots with LangGraph*. It is not the course's official exercise files.

## What can you ask it?

| Type this in the chat | What you should see |
| --- | --- |
| `What is the price of Nova headphones?` | The sample price: ₹2,499 |
| `What about its warranty?` | The Nova headphones' warranty: 1 year. Ask this after the first question. |
| `Where is order ORD1001?` | A made-up order status: shipped |
| `Summarize our chat` | A short recap of what you asked |

**Demo mode** uses simple rules and sample information. It does not call an AI service. You do not need an API key or payment details to try it.

## Run it on a Windows computer

You need Python installed and an internet connection for the first setup. If you do not have Python, [download it from python.org](https://www.python.org/downloads/).

### 1. Download the project

On this GitHub page, click the green **Code** button, then **Download ZIP**. Find the ZIP in Downloads, right-click it, and choose **Extract All**.

Open the extracted folder that contains `app.py` and `requirements.txt`.

### 2. Open Command Prompt in that folder

Click the address bar at the top of File Explorer, type `cmd`, and press **Enter**. A black Command Prompt window will open in the correct folder.

Type this and press **Enter** to check Python:

```bat
py --version
```

You should see a Python version number.

### 3. Set up the project (first time only)

Copy one line at a time into Command Prompt. Press **Enter** after each line. Wait for the second command to finish installing the packages.

```bat
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

The `.venv` folder holds the packages for this project. You do not need to open it or upload it to GitHub.

### 4. Start the chatbot

In the same Command Prompt window, run:

```bat
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Your browser should open the app. If it does not, open [http://localhost:8501](http://localhost:8501) yourself.

In the app, leave **Demo (no key needed)** selected. Type the four sample questions from the table above, one after another.

This app runs on your computer while Command Prompt is open. The `localhost` address is not a public website.

### 5. Stop or open it again later

To stop the app, go back to Command Prompt and press **Ctrl+C**.

To use it another day, open Command Prompt in the project folder again and run **only the command in Step 4**. You do not need to repeat the first-time setup.

If you already set up the project with a folder named `venv` instead of `.venv`, use this command to start it:

```bat
venv\Scripts\python.exe -m streamlit run app.py
```

## If something does not work

- **`py` is not recognized:** Install Python, then close and reopen Command Prompt.
- **`No module named streamlit`:** Run the second command in Step 3 again and wait for it to finish.
- **The browser did not open:** Visit [http://localhost:8501](http://localhost:8501) while Command Prompt is still running.
- **It asks for an API key:** Choose **Demo (no key needed)** in the app's sidebar.
- **An order is missing:** This practice shop only has sample orders `ORD1001`, `ORD1002`, and `ORD1003`.

## How does it work?

The program reads your question and sends it to the right part: product details, order status, chat recap, or a general reply.

It remembers earlier messages while the app is running. That is why you can ask “What about its warranty?” after asking about Nova headphones. Restarting the app clears that saved chat.

If you want to explore the files:

- `app.py` makes the chat screen.
- `bot.py` decides where questions go.
- `shop_data.py` contains the made-up products and orders.
- `START_HERE.md` explains more of the learning ideas.

## Optional: AI mode

You can complete and use this project in Demo mode. **AI (API key needed)** is optional. It calls the OpenAI API and may cost money. A ChatGPT subscription does not include API usage.

If you choose to use AI mode, check [OpenAI API billing](https://platform.openai.com/settings/organization/billing/overview) first. In Command Prompt in the project folder, run:

```bat
copy .env.example .env
notepad .env
```

In Notepad, put your API key after `OPENAI_API_KEY=`, save the file, and restart the app using Step 4. Then choose **AI (API key needed)**.

Keep `.env` private. Do not upload it to GitHub or share it in screenshots.
