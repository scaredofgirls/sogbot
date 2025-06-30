# Sogbot
## About
This is my discord bot, that I am writing for my own usage.

Feel free to use it for whatever reason you choose.

That said, this is not some community project or thing being done "for posterity" or some such non-sense.

Found a bug?

1. Submit an issue.
2. I may very well just close it.
3. Submit it with a PR fixing it? I may very well just merge it.

Have an idea for new functionality?
1. Submit an issue.
2. If it's not functionality that I think I would use, personally, I may very well just close it.
3. You're free to fork the repo, and just add the functionality you want!

## Installation
Clone this repository.
Create a new python virtual environment and activate it.

    python3 -m venv ./.venv
    source .venv/bin/activate

Install the required dependencies.

    pip install -r requirements.txt

Create a configuration file, then edit it:

    cp config.yaml.dist config.yaml
    vim config.yaml

Start the bot:

    ./bot.py
