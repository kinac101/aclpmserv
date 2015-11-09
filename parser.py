#!/usr/bin/env python

__author__ = ["Mathias Beke", "kinac101"]

"""
Simple script for parsing logs generated by the Assault Cube server
"""
import datetime
import json
import jsonpickle
import re
import sys
import time as ttt

class Player:
    """
    Data structure for a player
    """
    
    def __init__(self):
        self.name = ""
        self.ip = ""
        self.visits = 0
        self.time = 0
        self.killactions = {}
        self.flagactions = {}
        self.kills = 0
        self.killed = 0
        self.teamkills = 0
        self.teamkilled = 0
        self.flagteamkills = 0
        self.flagteamkilled = 0
        self.suicides = 0
        self.lastseen = 0

    def incrementKillAction(self, action):
        if self.killactions.has_key(action):
            self.killactions[action] += 1
        else:
            self.killactions[action] = 1
            
    def incrementFlagAction(self, action):
        if self.flagactions.has_key(action):
            self.flagactions[action] += 1
        else:
            self.flagactions[action] = 1
            
    def decrementFlagAction(self, action):
        if self.flagactions.has_key(action):
            self.flagactions[action] -= 1
        else:
            self.flagactions[action] = 0

class LogParser:
    """
    Class for parsing logfiles generated by the Assault Cube server
    """

    def __init__(self):
        self.players = {}
        self.killActions = [
            "busted",
            "picked off",
            "peppered",
            "sprayed",
            "punctured",
            "shredded",
            "slashed",
            "splattered",
            "headshot",
            "gibbed",
            "suicided"
        ]
        self.flagActions = [
            "scored",
            "returned",
            "lost",
            "stole",
            "dropped",
            "hunted",
            "forced to pickup",
            "carrying"
        ]
        self.flagbearer = None        
        self.teamkillMessage = "their teammate"
        self.suicideMessage = "suicided"
        self.playerConnected = "logged in"
        self.playerDisconnected = "disconnected client"
        self.patternLine = re.compile("\[[0-9\.]*\]")
        self.total = {
            "kills" : 0,
            "teamkills" : 0,
            "suicides" : 0
        }
        self.timestamp = 0

    def getPlayer(self, name):
        if name in self.players:
            return self.players[name]
        else:
            player = Player()
            player.name = name
            self.players[name] = player
            return self.players[name]
        
    def parseline(self, line):
        if "Status at " in line:
            items = line.split(" ")
            [datestr, timestr] = items[2:4]
            dd, mn, yy = map(int, datestr.split("-"))
            timeinfo = timestr.split(":")
            if timeinfo[-1] == "":
                del timeinfo[-1]
            hh, mi, sc = map(int, timeinfo)
            dtinfo = datetime.datetime(yy, mn, dd, hh, mi, sc)
            self.datetime = dtinfo
            self.timestamp = ttt.mktime(dtinfo.timetuple())
        if self.patternLine.match(line):
            items = line.split()
            actor = ""
            target = ""
            teamkill = False
            # Line too short, we're not interested
            if len(items) > 2:
                actor = items[1]
                target = items[-1]
            else:
                return
            if line.find(self.playerConnected) >= 0:
                self.getPlayer(actor).ip = items[0][1:-1]
                return
            elif line.find(self.playerDisconnected) >= 0:
                actor = items[3]
                if actor == "cn":
                    return
                time = int(items[6])
                self.getPlayer(actor).visits += 1
                self.getPlayer(actor).time += time
                self.getPlayer(actor).lastseen = self.timestamp
                return
            for a in self.killActions:
                if line.find(a) >= 0:
                    self.total["kills"] += 1
                    if a == self.suicideMessage:
                        self.getPlayer(actor).suicides += 1
                        self.total["suicides"] += 1
                    else:
                        self.getPlayer(actor).incrementKillAction(a)
                        self.getPlayer(actor).kills += 1
                        self.getPlayer(target).killed += 1
                        if line.find(self.teamkillMessage) >= 0:
                            self.getPlayer(actor).teamkills += 1
                            self.getPlayer(target).teamkilled += 1
                            self.total["teamkills"] += 1
                            if self.flagbearer == target:
                                self.getPlayer(actor).flagteamkills += 1
                                self.getPlayer(target).flagteamkilled += 1
                                self.flagbearer = None
                    if self.getPlayer(actor).ip == "":
                        self.getPlayer(actor).ip = items[0][1:-1]
                            
            for a in self.flagActions:
                if line.find(a) >= 0:
                    self.getPlayer(actor).incrementFlagAction(a)
                    if a in ["carrying"]:
                        self.getPlayer(actor).decrementFlagAction("scored")
                    
                    if a in ["stole","forced to pickup"]:
                        self.flagbearer = actor
                    else:
                        self.flagbearer = None
                    if self.getPlayer(actor).ip == "":
                        self.getPlayer(actor).ip = items[0][1:-1]

    def __getstate__(self):        
        return {"total": self.total, "players": self.players}

if __name__ == "__main__":
    p = LogParser()
    for line in sys.stdin:
        p.parseline(line)
    output = json.dumps(json.loads(jsonpickle.encode(p, unpicklable=False)),
                        indent=4)
    print output
