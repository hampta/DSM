# Discord Server Monitoring #
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/hampta/DSM)

## Information ##
All games on the Source (CSS, CSGO) and GoldSource (HL1DM, CS 1.6) engines are supported.

- Auto update once a minute
- Manual update
- Easy to use


## Usage ##
### Commands ###
It has just four commands:

* `!add <ip>:<*port>` — add specified IP:port to your watchlist so bot will check those servers every 2 minutes and notify you with those IP:ports if one of them (or more) go down
* `!remove <ip>:<*port>` — removes certain server from your watchlist
* `!help` - help message

\* - optional (defalut value is 27015
## Installation ##
### Requirements ### 
python 3.8+ with latest packages:

* discord.py
* tortoise-orm
* SQLite or PostgresSQL

### Actually installing & running ###
**Windows**:
```
git clone http://github.com/hampta/DSM
cd DSM
pip install -r requirements.txt
python main.py
```
**Linux**:
```
git clone http://github.com/hampta/DSM
cd DSM
pip3 install -r requirements.txt
python3 main.py
```
Now go to [this page](https://discordapp.com/developers/applications/me/create), log in and create an application (application name is not bot’s name, but the image will be used as your bot’s avatar), then create a bot user & give it a name, save, click on „click to reveal“ near the „Token:“, copy the token.  
Navigate to the root folder of downloaded repo, open `config.py` with any text editor. Save the file and close it.
 
Last step: go back to the application page and copy the **Client ID**, then replace `CLIENT_ID_GOES_HERE` with the actual Client ID in this link: `https://discordapp.com/api/oauth2/authorize?client_id=CLIENT_ID_GOES_HERE&scope=bot&permissions=0`. Visit it and select the server you want your bot to join. Bam, done.
