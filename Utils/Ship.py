from Utils.BattleUnit import BattleUnit

class CapitalShip(BattleUnit):
    # parent of all capital ships
    _DEFAULT_HP = 30
    _DEFAULT_ATK = 2
    _DEFAULT_MP = 2
    def __init__(self, pos, hp=_DEFAULT_HP, atk=_DEFAULT_ATK, mp=_DEFAULT_MP):
        super(CapitalShip, self).__init__(pos, hp, atk, mp)
    
    def __repr__(self):
        return f'Capital({self._current_hp}-{self._base_atk+self._bouns_atk}-{self._current_mp}) - {self._artillery}'



class WarShip(BattleUnit):
    # parent of all warships
    _DEFAULT_MP = 1
    def __init__(self, pos, hp, atk, mp=_DEFAULT_MP):
        super(WarShip, self).__init__(pos, hp, atk, mp)

    def __repr__(self):
        return f'WarShip({self._current_hp}-{self._base_atk+self._bouns_atk}-{self._current_mp}) - {self._artillery}'
