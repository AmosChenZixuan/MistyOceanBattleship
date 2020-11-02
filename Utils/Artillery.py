from Utils.Board import Board

class Artillery:
    def __init__(self, load_time):
        self.load_counter = load_time

    def ready(self):
        return self.load_counter <= 0

    def update(self):
        if not self.ready():
            self.load_counter -= 1
        return self.load_counter
    
    def __repr__(self):
        return f'{str(type(self))[24:-2]}({self.load_counter})'

class TypeZero(Artillery):
    # Single Target
    #  -----
    #  | T |
    #  -----
    damage = 3
    load_time = 0
    cost = 1
    def __init__(self):
        super(TypeZero, self).__init__(self.load_time)
    
    def get_range(self, target):
        return [target]

class TypeOne(Artillery):
    # Two Targets
    #  ---------
    #  | T |   |
    #  ---------
    damage = 1
    load_time = 0
    cost = 2
    def __init__(self):
        super(TypeOne, self).__init__(self.load_time)
    
    def get_range(self, target):
        arange = [target]
        if (target+1) % Board._X != 0:
            arange.append(target + 1)
        return arange

class TypeTwo(Artillery):
    # Two Targets
    #  -----
    #  | T |
    #  -----
    #  |   |
    #  -----
    damage = 1
    load_time = 0
    cost = 2

class TypeThree(Artillery):
    # Four Targets
    #  ---------
    #  | T |   |
    #  ---------
    #  |   |   |
    #  ---------
    damage = 1
    load_time = 1
    cost = 3

class TypeFour(Artillery):
    # Four Targets
    #      -----
    #      |   |
    #  -------------
    #  |   | T |   |
    #  -------------
    #      |   |
    #      -----
    damage = 0
    load_time = 2
    cost = 3

INV_MAP = {0: TypeZero,
            1: TypeOne,
            2: TypeOne,
            3: TypeOne,
            4: TypeOne}

