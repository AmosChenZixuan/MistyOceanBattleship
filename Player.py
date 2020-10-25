from Utils.Board import *
from Utils.Ship import *
# from Utils.Card import *

class Player:
    _BASE_FUEL = 3
    _FUEL_CAP = 10
    _FUEL_BANK_CAP = 3
    _HAND_CAP = 10

    def __init__(self, ships:['ships'], deck:['cards'], mode = 'default'):
        self._board = Board(mode=mode)
        self._ships = ships
        self._deck = deck

        self._hand = []
        self._fuel = self._BASE_FUEL
        self._fuel_bank = 0
        self._opponent = None

    def consume(self, amount, useBank=True):
        bank, fuel = self.getFuel()
        total_available = fuel + (0 if not useBank else bank)
        if amount > total_available:
            return False
        # use bank first
        fianl_cost = amount - bank
        if fianl_cost < 0:
            self._fuel_bank -= amount
        else:
            self._fuel_bank = 0
            self._fuel -= fianl_cost
        return True

    def set_opponent(self, opp):
        self._opponent = opp
    
    def get_opponent(self):
        return self._opponent

    def storeFuel(self):
        # called at round end, store unused fuel to bank
        if (self._fuel > 0):
            self._fuel_bank = min(3, self._fuel_bank + self._fuel)
            self._fuel = 0

    def refill(self, round):
        # called at round start, refill fuel
        self._fuel = min(self._BASE_FUEL + round -1, self._FUEL_CAP)

    def update(self):
        # called at round end
        self._board.update()
        
        # TO-DO  结算船的被动技能的回合结束效果，如果有的话

    def getBoard(self):
        return self._board.getBoard()

    def getPos(self):
        # [capital war1 war2]
        ships = self._ships
        return [ships[i].at() for i in range(3)]
    
    def getFuel(self):
        return (self._fuel_bank, self._fuel)

    
