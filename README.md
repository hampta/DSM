# Discord Server Monitoring #


[![Discord Bots](https://top.gg/api/widget/927577563998617641.svg)](https://top.gg/bot/927577563998617641)


## Information ##
### What is Server Monitoring bot ###
A python discord bot that queries Source and GoldSrc servers and notifies those who added several servers to their watchlists if those servers are currently down. Pretty simple. It is also capable of showing you detailed information such as:

* Hostname
* Current map
* VAC status
* Amount of players on server


## Usage ##
### Commands ###
It has just four commands:

* `!add <ip>:<*port>` — add specified IP:port to your watchlist so bot will check those servers every 2 minutes and notify you with those IP:ports if one of them (or more) go down
* `!remove <ip>:<*port>` — removes certain server from your watchlist
* `!help` - help message

## Installation ##
### Requirements ###
**Hardware:** not a toster and a decent hard drive.  
**Software:** python 3.8+ with latest packages:

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
