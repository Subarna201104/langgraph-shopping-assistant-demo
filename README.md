Shopping Assistant Demo
This is a small practice chatbot that runs in your web browser. It can answer questions about a made-up shop. The products and orders are examples, so it cannot check a real order or sell anything.
The project was inspired by the ideas in LinkedIn Learning's Build AI Agents and Chatbots with LangGraph. It is an original practice project, not the course's official exercise files.
What can you ask it?
Type this in the chat	What you should see
What is the price of Nova headphones?	The sample price: ₹2,499
What about its warranty?	The Nova headphones' warranty: 1 year. Ask this after the first question.
Where is order ORD1001?	A made-up order status: shipped
Summarize our chat	A short recap of what you asked


The Demo setting uses simple rules and sample information. It does not call an AI service, and you do not need an API key or payment details to try it. The optional AI setting is explained near the end.
Run it on a Windows computer
You need Python installed and an internet connection for the first setup. If you do not have Python, download it from python.org. You do not need to know Python to follow these steps.
1. Download the project
On this GitHub page, click the green Code button, then Download ZIP. Find the ZIP in Downloads, right-click it, and choose Extract All. Open the extracted folder that contains app.py and requirements.txt.
2. Open Command Prompt in that folder
Click the address bar at the top of File Explorer, type cmd, and press Enter. A black Command Prompt window will open in the correct folder.
Type this and press Enter to check Python:
py --version
You should see a Python version number. If Windows says py is not recognized, install Python and reopen Command Prompt.
3. Set up the project (first time only)
Copy one line at a time into Command Prompt and press Enter after each line. Wait for the second command to finish downloading and installing the packages.
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
The .venv folder holds this project's Python packages. You do not need to open it or upload it to GitHub.
4. Start the chatbot
In the same Command Prompt window, run:
.\.venv\Scripts\python.exe -m streamlit run app.py
Your browser should open the app. If it does not, open http://localhost:8501 yourself. This address works on your computer while the program is running; it is not a public website.
In the app, leave Demo (no key needed) selected. Type the four sample questions from the table above, one after another. You can click Start a new chat to clear the conversation.
5. Stop or reopen it later
To stop, return to Command Prompt and press Ctrl+C. To use it another day, open Command Prompt in the project folder again and run only the command in Step 4. You do not need to repeat the first-time setup.
Already set it up with a folder named venv (without the dot)? Use venv\Scripts\python.exe -m streamlit run app.py instead of the Step 4 command.
If something does not work
- No module named streamlit: Run the second command in Step 3 again and wait for it to finish.
- The browser did not open: Visit http://localhost:8501 while Command Prompt is still running.
- It asks for an API key: In the app's sidebar, choose Demo (no key needed).
- An order is missing: This practice shop only has the sample order IDs ORD1001, ORD1002, and ORD1003.
What is LangGraph doing here?
The program reads your question and sends it to the right part: product details, order status, chat recap, or a general reply. It remembers earlier messages during the current run, which lets you ask “What about its warranty?” after asking about Nova headphones. Closing and restarting the app clears that saved chat.
If you want to explore the files, app.py makes the chat screen, bot.py decides where questions go, and shop_data.py contains the made-up product and order information. START_HERE.md explains more of the learning ideas.
Optional: use the AI setting
You can finish this project using Demo mode. The AI (API key needed) setting makes calls to the OpenAI API. It needs your own API key and may cost money; a ChatGPT subscription does not include API usage.
If you choose to use it, check OpenAI API billing first. In Command Prompt in the project folder, run:
copy .env.example .env
notepad .env
In Notepad, paste your API key after OPENAI_API_KEY=, save the file, close Notepad, and restart the app using Step 4. Then choose AI (API key needed) in the sidebar. Keep .env private: do not upload it to GitHub or share it in screenshots.
