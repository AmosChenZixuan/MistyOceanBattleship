from Game import Game
from Player import Player
from Utils.Ship import *

def request_formation(name):
    pos = []
    while len(pos)!=3:
        pos = input(f"Enter Initial positions for {name} (Capital, war1, war2):").split() 
        pos = list(map(lambda x:int(x), pos))
    
    assert all([x <= 24 for x in pos])
    print(f'Positions for {name}', pos)
    return pos

if __name__ == '__main__':
    # before game, request formation and deck selection
    pos1 = request_formation('player1')
    pos2 = request_formation('player2')

    ships1 = [CapitalShip(pos1[0]), WarShip(pos1[1], 20, 10), WarShip(pos1[2], 50, 5)]
    ships2 = [CapitalShip(pos2[0]), WarShip(pos2[1], 20, 10), WarShip(pos2[2], 50, 5)]

    deck1 = []
    deck2 = []

    player1 = Player('player1', ships1, deck1)
    player2 = Player('player2', ships2, deck2)

    # init game
    game = Game(player1, player2)

    acitons = {'next': game.next_round,
                'test': game.Test_random_dissipate,
                'move': game.move,
                'attack': game.attack,
                'atk': game.attack,
                'quit': game.gameover}

    while game.isRunning():
        game.draw()
        try:
            cmd = input("Your move:").split()
            action = acitons[cmd[0]]
            args = cmd[1:]
            action(*args)
        except(KeyError):
            print('Invalid Move')
        except:
            print('Command Failed')

        
    
