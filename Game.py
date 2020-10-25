from Utils.Board import Board
class Game:
    def __init__(self, player1, player2):
        player1.set_opponent(player2)
        player2.set_opponent(player1)

        self._players = [player1, player2]
        self._round_counter = 1
        self._round_token = player1   # current turn belongs to playerX who holds the token
        self._running = True
    
    def isRunning(self):
        return self._running

    def gameover(self):
        self._running = False

    def next_round(self):
        self.current_player().storeFuel()
        for p in self._players:
            p.update()
        self._round_counter += 1
        self._round_token = self._players[self._round_counter%2 - 1]
        self._round_token.refill(self._round_counter)
        # TO-DO draw cards for both players 
        # TO_DO trigger some ship's round-start effect

    
    def current_turn(self):
        return self._round_counter

    def current_player(self):
        return self._round_token

    def draw(self):
        print("Current Round:", self.current_turn())
        cur_board = self.current_player().getBoard()
        opp_board = self.current_player().get_opponent().getBoard()

        cur_pos = self.current_player().getPos()
        opp_pos = self.current_player().get_opponent().getPos()

        # render ships
        cur_board[cur_pos[0]].setDisplay('capital', seeThrough=True)
        cur_board[cur_pos[1]].setDisplay('warship1', True)
        cur_board[cur_pos[2]].setDisplay('warship2', True)

        opp_board[opp_pos[0]].setDisplay('capital', seeThrough=False)
        opp_board[opp_pos[1]].setDisplay('warship1', False)
        opp_board[opp_pos[2]].setDisplay('warship2', False)

        # draw board
        index = 0
        for _ in range(Board._Y):
            print(cur_board[index:index+Board._X], end='       ')
            print(opp_board[index:index+Board._X])
            index += Board._X

        bank, fuel = self.current_player().getFuel()
        opp_bank, opp_fuel = self.current_player().get_opponent().getFuel()
        print(f"Bank[{bank}]               Bank[{opp_bank}]")
        print(f"Fuel[{fuel}]               Fuel[{opp_fuel}]")
        print('\n=====================\n')

    def Test_random_dissipate(self):
        # test method, randomly dissipate two blocks for both player. cost two fuel
        import random
        response = self.current_player().consume(2, useBank=True)
        if response:
            x,y = random.sample(range(25), 2)
            cur_board = self.current_player().getBoard()
            cur_board[x].dissipate()
            cur_board[y].dissipate()
            x,y = random.sample(range(25), 2)
            opp_board = self.current_player().get_opponent().getBoard()
            opp_board[x].dissipate()
            opp_board[y].dissipate()
        else:
            print("not enough fuel. Oops")





if __name__ == '__main__':
    g = Game('1', '2')

    for i in range(5):
        print(g.current_turn(), g.current_player())
        g.next_round()