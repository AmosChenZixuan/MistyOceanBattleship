from Utils.Board import Board
class BattleUnit:
    # Abstract unit on the borad
    def __init__(self, pos, hp, atk, mp):
        # pos: initial position on the borad
        # hp: max health
        # atk: initial attack power
        # mp: max mobility 

        # static stats
        self._base_hp = hp
        self._base_atk = atk
        self._base_mp = mp

        # dynamic stats
        self._bouns_atk = 0
        self._current_hp = hp
        self._current_mp = mp
        #self._armor = 0
        self._pos = pos

        # status
        #self._status = []  # 封刃，封足，等
        #self._shielded = False
        self._artillery = None

    def ableAttck(self):
        # To-DO : define artillery class and 'disarm' status
        if not self.isAlive():
            return False
        if self._artillery == None:
            return True
        else:
            return self._artillery.ready()

    def isAlive(self):
        return self._current_hp > 0

    def at(self):
        return self._pos

    def takeDamage(self, val):
        # future: armors, shields
        if self.isAlive():
            self._current_hp -= val
        return self._current_hp
    
    def refill(self):
        # refill mp, update load counter
        if self.isAlive():
            self._current_mp = self._base_mp
            self._bouns_atk = 0
            if self._artillery:
                self._artillery.update()

    def move(self, direction, forbid_pos):
        # direction: 'up' / 'down' / 'left' / 'right'
        status = False
        if self._current_mp <= 0 or not self.isAlive():
            return status
        x = Board._X
        y = Board._Y
        # make move
        notTaken = lambda x: x not in forbid_pos

        if direction == 'up' and self._pos >= x:
            new_pos = self._pos - x
            status = notTaken(new_pos)
        elif direction == 'down' and self._pos < x*(y-1):
            new_pos = self._pos + x
            status = notTaken(new_pos)
        elif direction == 'left' and self._pos % x != 0:
            new_pos = self._pos - 1
            status = notTaken(new_pos)
        elif direction == 'right' and self._pos % x != (x-1):
            new_pos = self._pos + 1
            status = notTaken(new_pos)
        # return
        if status:
            self._current_mp -= 1
            self._pos = new_pos
        return status

    def attack(self, target_idx):
        if self._artillery == None:
            return (self._base_atk + self._bouns_atk, [target_idx])
        else:
            damage = self._artillery.damage + self._base_atk + self._bouns_atk
            arange = self._artillery.get_range(target_idx)
            self._artillery = None
            return (damage, arange)
    
    def equip(self, artillery):
        self._artillery = artillery

    
    


