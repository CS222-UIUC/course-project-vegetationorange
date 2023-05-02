# Stonks
Students often have keen interests in financial literacy but lack the funds to have real world experience. Stonks lets students have a gamified (competitive) yet safe space to learn how the stock market functions by trading while competing against other students. Students start with a set amount of money, and they are allowed to buy and sell publicly-traded stocks as they see fit. They can lookup stocks via a page on our web app, and they can check their standings with the leaderboard.

While similar projects exist, our solution is highly user-friendly with a focus on modern design and quick actions. This makes the idea of stock trading more approachable to people new to the topic.

## Built With
1. Flask (backend)
2. Firebase (database)
3. Finnhub as Public Stock API (data)
4. Bootstrap and Jinja templates (frontend)


## Setup
1. Acquire project permissions
2. Clone the project onto your computer
3. Download necessary tools
    1. Python 3.10
    2. IDE of choice (Ex. Visual Studio Code)
    3. Set up virtual environment (isolates project python and libraries)
        1. Easy with VSCode, just install Python extension and create a new virtual environment from the command palette.
            1. Choose the correct Python version, select requirements.txt to import all necessary libraries, and you're set.
        2. Alternatively install requirements globally or isolated manually (not recommended unless you know what you're doing)
4. To start up the project, launch virtual environment (default after setup in VSCode) and run ```python3 server.py ```.
5. Once the server starts up, click the link in the terminal to open the Stonks app in your browser. You're all set!

Developed by Shlok Mehrotra, Ritvik Banakar, Anay Bhakat, and Sayan Sisodiya. All four members worked on the frontend and backend.
