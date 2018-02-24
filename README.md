# SteamParty
Get common games between Steam users to find out which game is going to be tonight's theme!

## Usage
```
./SteamParty.py user_id1 user_id2...
```

where `user_id` can be either custom profile name or a numeric ID.

Example output (without colors):
```
$ ./SteamParty.py mrc0mmand 765XXXXXXXXX another_user
2018-02-24 16:07:39,140 [SteamParty/get_games] INFO: http://steamcommunity.com/id/mrc0mmand/games/?tab=all
2018-02-24 16:07:39,140 [SteamParty/get_games] INFO: Fetching games for user mrc0mmand
2018-02-24 16:07:43,989 [SteamParty/get_games] INFO: http://steamcommunity.com/profiles/765XXXXXXXXX/games/?tab=all
2018-02-24 16:07:43,989 [SteamParty/get_games] INFO: Fetching games for user 765XXXXXXXXX
2018-02-24 16:07:45,288 [SteamParty/get_games] INFO: http://steamcommunity.com/id/another_user/games/?tab=all
2018-02-24 16:07:45,288 [SteamParty/get_games] INFO: Fetching games for user another_user
(Win: yes, Linux: yes, OS/X: yes) [F2P: no , MP: yes, Co-op: yes] Monaco
(Win: yes, Linux: no , OS/X: yes) [F2P: no , MP: no , Co-op: no ] Grand Theft Auto: San Andreas
(Win: yes, Linux: no , OS/X: yes) [F2P: yes, MP: yes, Co-op: yes] Realm of the Mad God
(Win: yes, Linux: yes, OS/X: yes) [F2P: yes, MP: yes, Co-op: yes] No More Room in Hell
(Win: yes, Linux: no , OS/X: no ) [F2P: no , MP: no , Co-op: yes] Sniper Elite: Nazi Zombie Army
(Win: yes, Linux: yes, OS/X: yes) [F2P: no , MP: yes, Co-op: no ] Counter-Strike: Source
(Win: yes, Linux: yes, OS/X: yes) [F2P: yes, MP: yes, Co-op: no ] Fistful of Frags
(Win: yes, Linux: yes, OS/X: yes) [F2P: yes, MP: no , Co-op: no ] Unturned
(Win: yes, Linux: yes, OS/X: yes) [F2P: no , MP: yes, Co-op: yes] Garry's Mod
(Win: yes, Linux: yes, OS/X: yes) [F2P: no , MP: yes, Co-op: yes] Serious Sam 3: BFE
(Win: yes, Linux: yes, OS/X: yes) [F2P: yes, MP: yes, Co-op: no ] Team Fortress 2
(Win: yes, Linux: yes, OS/X: yes) [F2P: no , MP: no , Co-op: yes] Borderlands 2
(Win: yes, Linux: yes, OS/X: yes) [F2P: no , MP: yes, Co-op: yes] Left 4 Dead 2
(Win: yes, Linux: yes, OS/X: yes) [F2P: no , MP: yes, Co-op: yes] Serious Sam Fusion 2017 (beta)
(Win: yes, Linux: yes, OS/X: yes) [F2P: no , MP: no , Co-op: yes] Portal 2
(Win: yes, Linux: no , OS/X: no ) [F2P: yes, MP: yes, Co-op: yes] Alien Swarm
(Win: yes, Linux: no , OS/X: no ) [F2P: no , MP: yes, Co-op: yes] Sniper Elite V2
```

As this script needs to fetch game info for each game separately, it can take several minutes when run for the first time.
The structure with the game data is saved after every game info update to make subsequent runs faster. If you notice
that some game info data is incorrect, simply delete the cache (file `.SteamParty.cache`) to force re-fetch of all game
info data.

## Required packages (Python 3)
* colorama
* requests
