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

    ships1 = [CapitalShip(pos1[0]), WarShip(pos1[1], 20, 5), WarShip(pos1[2], 20, 5)]
    ships2 = [CapitalShip(pos2[0]), WarShip(pos2[1], 20, 5), WarShip(pos2[2], 20, 5)]

    deck1 = []
    deck2 = []

    player1 = Player(ships1, deck1)
    player2 = Player(ships2, deck2)

    # init game
    game = Game(player1, player2)

    acitons = {'next': game.next_round,
                'test': game.Test_random_dissipate,
                'quit': game.gameover}

    while game.isRunning():
        game.draw()
        try:
            action = acitons[input("Your move:")]
            action()
        except(KeyError):
            print('Invalid Move')
        
        
    
