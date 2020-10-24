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
        self._armor = 0
        self._pos = pos

        # status
        self._status = []  # 封刃，封足，等
        self._shielded = False
        self._artillery = None

    def ableAttck(self):
        # To-DO : define artillery class and 'disarm' status
        if self._artillery == None:
            return True
        else:
            return True

    def isAlive(self):
        return self._current_hp > 0

    def at(self):
        return self._pos
    
    


