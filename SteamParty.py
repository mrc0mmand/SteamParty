#!/usr/bin/env python3

import json
import logging
import pickle
import re
import requests
import sys
from colorama import Fore, Style
from time import sleep

class SteamGrabber:
    """Interface for fetching user/application data from the Steam servers"""
    def __init__(self):
        # Format: appid : name
        self._games = {}
        self._profile_template = "http://steamcommunity.com/{}/{}/games/?tab=all"
        self._app_template = "http://store.steampowered.com/api/appdetails?appids={}"
        self._content_rx = re.compile(r"var rgGames[ ]*=[ ]*(\[.+\])")

        # If a game cache exists try to load it
        try:
            with open(".SteamParty.cache", "rb") as fin:
                self._games = pickle.load(fin)
        except FileNotFoundError:
            logging.warning("No local cache found, fetching data may take some time")

    def _fetch(self, url):
        """Fetch content from given URL.

        Parameters
        ---------
        url : str
            URL to fetch content from

        Returns
        -------
        str
            Fetched content of the given URL converted to UTF-8 string

        """
        try:
            res = requests.get(url)
        except:
            logging.exception("Failed to fetch data")
            return None

        if res.status_code == 200:
            return str(res.content, encoding="utf-8")
        else:
            logging.error("Check your connection (status code: {})".format(
                res.status_code))

        return None

    def get_app_info(self, appid):
        """Get information about application specified by its ID.

        Parameters
        ---------
        appid : int/str
            Application ID

        Returns
        -------
        bool
            True if fetching and parsing application info succeeds,
            False otherwise

        """
        url = self._app_template.format(appid)
        logging.debug(f"Fetching info for appid {appid}")
        logging.debug(url)

        data = self._fetch(url)

        if data is None:
            return False

        try:
            jdata = json.loads(data)
        except:
            logging.exception("Failed to parse JSON data")
            return False

        if not appid in jdata:
            logging.debug("Received response with invalid appid")
            return False

        try:
            game = jdata[appid]["data"]
        except:
            logging.debug(f"Missing 'data' section in the response: {jdata}")
            return False

        self._games[appid]["is_free"] = game["is_free"]
        self._games[appid]["platforms"] = game["platforms"]
        # Category ID 9 - Co-op
        self._games[appid]["coop"] = any(x["id"] == 9 for x in game["categories"])
        # Category ID 1 - Multiplayer
        self._games[appid]["mp"] = any(x["id"] == 1 for x in game["categories"])

        return True

    def get_game_info(self, appid):
        """Get application info from the local cache.

        Parameters
        ----------
        appid : int/str
            Application ID

        Returns
        -------
        dict
            Application info dictionary if it exists in the local cache,
            None otherwise
        """
        if appid in self._games:
            return self._games[appid]
        else:
            return None

    def get_games(self, userid):
        """Get games from a user profile specified by given ID.

        Parameters
        ----------
        userid : str
            Either custom profile name or numeric ID

        Returns
        -------
        set
            Set of application IDs on success, None otherwise
        """
        if userid.isdigit():
            type_ = "profiles"
        else:
            type_ = "id"

        url = self._profile_template.format(type_, userid)
        logging.info(url)
        logging.info(f"Fetching games for user {userid}")

        data = self._fetch(url)

        if data is None:
            return None

        # Parse JSON string with games from the HTML content (oh yes)
        match = re.search(self._content_rx, data)
        if match is None:
            logging.error("Failed to parse response data")
            print(data)
            return None

        try:
            jdata = json.loads(match.group(1))
        except:
            logging.exception("Failed to parse JSON data")
            return None

        games = []

        # Get application ID and application name from the JSON
        # If the application ID does not exist in the local cache,
        # fetch additional info from the Steam store
        for game in jdata:
            appid = str(game["appid"])
            if appid not in self._games:
                self._games[appid] = {}
                self._games[appid]["name"] = game["name"]
                sleep(0.2)
                if not self.get_app_info(appid):
                    del self._games[appid]
                    continue

            games.append(appid)

        with open(".SteamParty.cache", "wb") as fout:
            pickle.dump(self._games, fout, pickle.HIGHEST_PROTOCOL)

        return set(games)

if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO,
            format="%(asctime)-14s [%(module)s/%(funcName)s] %(levelname)s: %(message)s")
    logging.addLevelName(logging.INFO, "{}{}{}".format(Fore.GREEN,
                    logging.getLevelName(logging.INFO), Style.RESET_ALL))
    logging.addLevelName(logging.WARNING, "{}{}{}".format(Fore.YELLOW,
                    logging.getLevelName(logging.WARNING), Style.RESET_ALL))
    logging.addLevelName(logging.ERROR, "{}{}{}".format(Fore.RED,
                    logging.getLevelName(logging.ERROR), Style.RESET_ALL))
    logging.addLevelName(logging.CRITICAL, "{}{}{}".format(Fore.MAGENTA,
                    logging.getLevelName(logging.CRITICAL), Style.RESET_ALL))

    if len(sys.argv[1:]) == 0:
        print("Usage: {} steam_id steam_id2 ...".format(sys.argv[0]))
        sys.exit(0)

    grabber = SteamGrabber()
    # Format: username : games_set
    users = {}

    # Fetch games for each user
    for user in sys.argv[1:]:
        games = grabber.get_games(user)
        if games and len(games) > 0:
            users[user] = games
        else:
            logging.warning(f"Missing data for user {user}")

    common = set.intersection(*users.values())

    # Simple lambdas for colored text (used for yes/no flags)
    red = lambda x: "{}{:3}{}".format(Fore.RED, x, Style.RESET_ALL)
    green = lambda x: "{}{:3}{}".format(Fore.GREEN, x, Style.RESET_ALL)
    decide = lambda x: green("yes") if x else red("no")

    for appid in sorted(common):
        game = grabber.get_game_info(appid)
        if game is None:
            logging.warn(f"Missing info for appid {appid}")
            continue

        try:
            print("(Win: {}, Linux: {}, OS/X: {}) [F2P: {}, MP: {}, Co-op: {}] {}".format(
                    decide(game["platforms"]["windows"]),
                    decide(game["platforms"]["linux"]),
                    decide(game["platforms"]["mac"]),
                    decide(game["is_free"]),
                    decide(game["mp"]),
                    decide(game["coop"]),
                    game["name"]))
        except:
            logging.exception("Failed to print game data")
