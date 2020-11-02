from Utils.Board import *
from Utils.Ship import *
# from Utils.Card import *
from random import choice

class Player:
    _BASE_FUEL = 3
    _FUEL_CAP = 10
    _FUEL_BANK_CAP = 3
    _HAND_CAP = 2

    def __init__(self, id, ships:['ships'], deck:['cards'], mode = 'default'):
        self._id = id
        self._board = Board(mode=mode)
        self._units = ships
        self._deck = deck

        self._inventory = dict.fromkeys(range(5), 0)
        self._fuel = self._BASE_FUEL
        self._fuel_bank = 0
        self._opponent = None
    
    def getId(self):
        return self._id

    def consume(self, amount, useBank=True):
        bank, fuel = self.getFuel()
        total_available = fuel + (0 if not useBank else bank)
        if amount > total_available:
            return False
        if not useBank:
            self._fuel -= amount
            return True
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

    def get_unit(self, idx):
        return self._units[idx]
    
    def get_inv(self):
        return self._inventory

    def add2inv(self):
        not_full = [i for i in self._inventory if self._inventory[i] < self._HAND_CAP]
        if len(not_full) == 0:
            print("Full Inventory. Can not add more")
            return
        type_idx = choice(not_full)
        self._inventory[type_idx] += 1
        return self._inventory

    def storeFuel(self):
        # called at round end, store unused fuel to bank
        if (self._fuel > 0):
            self._fuel_bank = min(3, self._fuel_bank + self._fuel)
            self._fuel = 0

    def refill(self, round):
        # called at round start, refill fuel and update all units' status(mp, load counter)
        self._fuel = min(self._BASE_FUEL + round -1, self._FUEL_CAP)
        for unit in self._units:
            unit.refill()

    def update(self):
        # called at round end
        self._board.update()
        
        # TO-DO  结算船的被动技能的回合结束效果，如果有的话

    def getBoard(self):
        return self._board.getBoard()

    def getPos(self):
        # [capital war1 war2 ...]
        units = self._units
        return [units[i].at() for i in range(len(units))]
    
    def getFuel(self):
        return (self._fuel_bank, self._fuel)

    

