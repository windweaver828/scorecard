#!/usr/bin/env python

import sys, os
import pygame
from pgu import gui

GAMELIST = dict()

class Player(object):
    def __init__(self, name, phase=1, score=0):
        self.name = name
        self.phase = phase
        self.score = score
        
    def getText(self):
        return "{phase}-{name}: {score}".format(
            phase=self.phase,
            name=self.name,
            score=self.score)

class Phase10(gui.Desktop):
    def __init__(self, players):
        super(Phase10, self).__init__()
        self.name = "Phase 10"
        self.players = players
        self.dealer = 0
        self.winner = False
        self.playerwidth = 125
        self.width = len(self.players)*self.playerwidth
        self.height = 120
        pygame.display.set_mode((self.width, self.height))
        self.layout = gui.Container()#width=self.width, height=self.height)

        x = 15
        for player in players:
            player.scoreBox = gui.Input("", 6)
            self.layout.add(player.scoreBox, x+10, 30)
            x+= self.playerwidth

        nextButton = gui.Button("Next Round")
        self.layout.add(nextButton,
                        self.width-120, 70)
        resetButton = gui.Button("Reset")
        self.layout.add(resetButton,
                        self.width-195, 70)

        self.connect(gui.QUIT, self.onQuit)
        nextButton.connect(gui.CLICK, self.onNextRound)
        resetButton.connect(gui.CLICK, self.onReset)

        self.updatePlayerLabels(first=True)
        self.updateDealer()
        self.onReset()

    def onNextRound(self):
        winners = list()
        for player in self.players:
            try:
                value = int(player.scoreBox.value)
            except: value = 0
            player.score += value
            player.scoreBox.value = ""
            if value <= 50:
                player.phase += 1
            if player.phase == 11:
                winners.append(player)
        if len(winners):
            self.winner = min(winners, key=lambda x: x.score).name
            self.onQuit()
        if self.dealer == len(self.players)-1:
            self.dealer = 0
        else: self.dealer +=1
        self.updateAll()

    def onReset(self):
        for player in self.players:
            player.phase = 1
            player.score = 0
            player.scoreBox.value = ""
        self.dealer = 0
        self.updateAll()

    def updateAll(self):
        self.updatePlayerLabels()
        self.updateDealer()
      
    def updatePlayerLabels(self, first=False):
        if not first:
            for label in self.playerLabels:
                self.layout.remove(label)
        self.playerLabels = list()
        x = 15
        for player in self.players:
            label = gui.Label(player.getText())
            self.playerLabels.append(label)
            self.layout.add(label, x, 5)
            x+=self.playerwidth
            
    def updateDealer(self):
        text = "Dealer: {name}".format(name=self.players[self.dealer].name)
        pygame.display.set_caption(text)

    def start(self):
        self.run(self.layout)
    
    def onQuit(self):
        self.quit(None)
GAMELIST['Phase 10'] = Phase10

class GetGameDialog(gui.Desktop):
    def __init__(self, games):
        super(GetGameDialog, self).__init__()
        self.games = games
        self.value = False
        self.width = 200
        self.height = 100
        pygame.display.set_caption("Pick a game...")
        pygame.display.set_mode((self.width, self.height))
        self.layout = gui.Container()
        self.SelectBox = gui.Select()
        for game in self.games.keys():
            self.SelectBox.add(game, self.games[game])
            
        self.layout.add(self.SelectBox, 5, 0)
        okbutton = gui.Button("Ok")
        self.layout.add(okbutton, 150, 0)

        self.connect(gui.QUIT, self.onQuit)
        okbutton.connect(gui.CLICK, self.onDone)

    def start(self):
        self.run(self.layout)

    def onDone(self):
        self.value = self.SelectBox.value
        if not self.value: return
        self.onQuit()

    def onQuit(self):
        self.quit(None)

class WinnerDialog(gui.Desktop):
    def __init__(self, winner, players):
        super(WinnerDialog, self).__init__()
        self.winner = winner
        self.players = players
        self.width = 200
        self.height = (len(self.players)+5)*40
        pygame.display.set_caption("Game Over")
        pygame.display.set_mode((self.width, self.height))
        self.layout = gui.Container()#width=self.width, height=self.height)
        
        label = "{winner} wins!".format(winner=self.winner)
        self.layout.add(gui.Label(label), 15, 15)

        y = 70
        for player in self.players:
            label = "{name}:{score}".format(
                name=player.name, score=player.score)
            self.layout.add(gui.Label(label), 15, y)
            y+=40
            
        newGameButton = gui.Button("New Game")
        restartGameButton = gui.Button("Restart Game")
        self.layout.add(newGameButton, 10, y)
        y+=40
        self.layout.add(restartGameButton, 0, y)

        self.connect(gui.QUIT, self.onQuit)
        newGameButton.connect(gui.CLICK, self.onNewGame)
        restartGameButton.connect(gui.CLICK, self.onRestartGame)

    def start(self):
        self.run(self.layout)

    def onQuit(self):
        self.value = False
        self.quit(None)
        pygame.quit()

    def onNewGame(self):
        self.value = "new"
        self.quit(None)

    def onRestartGame(self):
        self.value = "restart"
        self.quit(None)

def runGame(players, gameobj):
        game = gameobj(players)
        game.start()
        winner = game.winner
        if winner: return (winner, game.players)
        else: return False
        
def getGame():
    dlg = GetGameDialog(GAMELIST)
    dlg.start()
    game = dlg.value
    if game: return game
    else: return False

def main():
    pygame.init()
    players = [Player("James"),
               Player("Brandi"),
               Player("Keith"),
               ]

    game = None
    while True:
        if not game: game = getGame()
        if not game: break
        ret = runGame(players, game)
        if ret: winner, players = ret
        else: break
        dlg = WinnerDialog(winner, players)
        dlg.start()
        ret = dlg.value
        if not ret: break
        elif ret == "new": game = None
        

    pygame.quit()

if __name__ == "__main__":
##    main()
    try: main()
    except SystemExit:
        pass
    except KeyboardInterrupt:
        pass
    except Exception, e:
        if not str(e) == "display Surface quit":
            print(e)
