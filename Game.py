from Utils.Board import Board
from Utils.Artillery import *
import json
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

    def checkGameOver(self):
        is_running = self.current_player().get_unit(0).isAlive() and \
                self.current_player().get_opponent().get_unit(0).isAlive()
        self._running = is_running
        if not is_running:
            print("GameOver!")
            self.draw()
        return not is_running

    def gameover(self):
        self._running = False

    def next_round(self):
        self.current_player().storeFuel()
        for p in self._players:
            p.update()
        self._round_counter += 1
        self._round_token = self._players[self._round_counter%2 - 1]
        self._round_token.refill(self._round_counter)
        # recharge Artilleries for both player
        turn = (self._round_counter + 2) % 4
        if  turn == 1:
            self._players[0].add2inv()
            self._players[0].add2inv()
        elif turn == 0:
            self._players[1].add2inv()
            self._players[1].add2inv()
        # trigger some ship's round-start effect

    
    def current_turn(self):
        return self._round_counter

    def current_player(self):
        return self._round_token

    def draw(self):
        print('\n=====================\n')
        print("Current Round:", self.current_turn())
        player = self.current_player()
        opp = self.current_player().get_opponent()
        cur_board = player.getBoard()
        opp_board = opp.getBoard()

        cur_pos = player.getPos()
        opp_pos = opp.getPos()

        # clear old renders
        for i in cur_board:
            i.setDisplay()
        for i in opp_board:
            i.setDisplay()
        # render units

        for i in range(len(cur_pos)):
            title = 'capital' if i == 0 else f'warship{i}'
            if player.get_unit(i).isAlive():
                cur_board[cur_pos[i]].setDisplay(title, seeThrough=True)
        for i in range(len(cur_pos)):
            title = 'capital' if i == 0 else f'warship{i}'
            if opp.get_unit(i).isAlive():
                opp_board[opp_pos[i]].setDisplay(title, seeThrough=False)
        to_print_cur=player.get_board_json()
        to_print_opp=opp.get_board_json()
        # draw board
        print(f"[{player.getId()}]              [{opp.getId()}]")
        index = 0
        for _ in range(Board._Y):
            print(cur_board[index:index+Board._X], end='       ')
            print(opp_board[index:index+Board._X])
            index += Board._X

        bank, fuel = player.getFuel()
        opp_bank, opp_fuel = opp.getFuel()
        print(f"Bank[{bank}]               Bank[{opp_bank}]")
        print(f"Fuel[{fuel}]               Fuel[{opp_fuel}]")
        for i in range(3):
            print(f"{player.get_unit(i)}       {opp.get_unit(i)}")
        print('Inventory:')
        player_inv = player.get_inv()
        opp_inv = opp.get_inv()
        for i in range(len(player_inv)):
            print(f"Type{i}[{player_inv[i]}]             Type{i}[{opp_inv[i]}]")
        print('\n=====================\n')
        to_dump= {"cur_board": to_print_cur, "opp_board":to_print_opp, "bank":bank, "fuel":fuel,
                         "opp_bank":opp_bank, "opp_fuel":opp_bank, "your_captial": player.get_unit(0).to_string(),
                                    "your_warship1": player.get_unit(1).to_string(), "your_warship2": player.get_unit(2).to_string(),
                                            "opp_capital": opp.get_unit(0).to_string(), "opp_warship1 ": opp.get_unit(1).to_string(),
                                                    "opp_warship2": opp.get_unit(2).to_string(), "your_inventory": player_inv,
                                                            "opp_inventory": opp_inv}
        return to_dump

    def Test_random_dissipate(self):
        # test method, randomly dissipate two blocks for both player. cost two fuel
        import random
        response = self.current_player().consume(2, useBank=True)
        if response:
            '''x,y = random.sample(range(25), 2)
            cur_board = self.current_player().getBoard()
            cur_board[x].dissipate()
            cur_board[y].dissipate()'''
            x,y = random.sample(range(25), 2)
            opp_board = self.current_player().get_opponent().getBoard()
            opp_board[x].dissipate()
            opp_board[y].dissipate()

            '''self.current_player().get_unit(0).takeDamage(10)
            self.checkGameOver()'''
        else:
            print("not enough fuel. Oops")


    def move(self, unit_idx, direction):
        unit_idx = int(unit_idx)
        player = self.current_player()
        _, fuel = player.getFuel()
        status = False
        if fuel < 1:
            print("Failed to move. Not enought fuel")
        elif player.get_unit(unit_idx).move(direction, player.getPos()):
            status = True
            player.consume(1, useBank=False)
        else:
            print("Failed to move. You may have ran out of MP or invalid direction")
        return status

    def attack(self, unit_idx, target_index):
        unit_idx = int(unit_idx)
        target_index = int(target_index)
        player = self.current_player()
        opp = player.get_opponent()
        unit = player.get_unit(unit_idx)
        status = False
        if not unit.isAlive():
            print("Failed to attack. The unit is dead")
            return status
        elif not unit.ableAttck():
            print("Failed to attack. The unit is not ready")
            return status
        elif player.consume(3, useBank=False):
            damage, atk_range = player.get_unit(unit_idx).attack(target_index)
            #print(f"DEBUG: ATK-{damage}, Range-{atk_range}")
            # clear mists and form attack map
            opp_board = opp.getBoard()
            atk_map = dict.fromkeys(range(len(opp_board)), 0)
            for i in atk_range:
                opp_board[i].dissipate()
                atk_map[i] = damage
            #print("DEBUG:map",atk_map)
            # take damage
            opp_pos = opp.getPos()
            for i in range(len(opp_pos)):
                if not opp.get_unit(i).isAlive():
                    continue
                dmg = atk_map[opp_pos[i]]
                if  dmg != 0:
                    opp.get_unit(i).takeDamage(dmg)
                    print(f"Hit! {i} took {dmg} damage")
            self.checkGameOver()
            status = True
        else:
            print("Failed to attack. Not enough fuel")
        return status
    
    def equip(self, unit_idx, artillery_type):
        unit_idx = int(unit_idx)
        artillery_type = int(artillery_type)

        atype = INV_MAP[artillery_type]
        player = self.current_player()
        unit = player.get_unit(unit_idx)
        status = False
        if not unit.isAlive():
            print("Failed to equip. The unit is dead")
            return status
        elif player.get_inv()[artillery_type] <= 0:
            print("Failed to equip. The artillery is currently unavailable")
            return status
        elif player.consume(atype.cost, useBank = True):
            unit.equip(atype())
            player.get_inv()[artillery_type] -= 1
            status = True
        else:
            print("Failed to equip. Not enough fuel")
        return status
        











if __name__ == '__main__':
    g = Game('1', '2')

    for i in range(5):
        print(g.current_turn(), g.current_player())
        g.next_round()