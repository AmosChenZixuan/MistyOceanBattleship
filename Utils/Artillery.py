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
    
    def addAbove(self,target, arange):
        if target >= Board._X:
            arange.append(target - Board._X)
        return arange

    def addBelow(self, target, arange):
        if target < Board._X * (Board._Y-1):
            arange.append(target + Board._X)
        return arange

    def addRight(self, target, arange):
        if (target+1) % Board._X != 0:
            arange.append(target + 1)
        return arange
    
    def addLeft(self, target, arange):
        if target % Board._X != 0:
            arange.append(target - 1)
        return arange

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
    damage = 2
    load_time = 0
    cost = 2
    def __init__(self):
        super(TypeOne, self).__init__(self.load_time)
    
    def get_range(self, target):
        arange = [target]
        arange = self.addRight(target, arange)
        return arange

class TypeTwo(Artillery):
    # Two Targets
    #  -----
    #  | T |
    #  -----
    #  |   |
    #  -----
    damage = 2
    load_time = 0
    cost = 2
    def __init__(self):
        super(TypeTwo, self).__init__(self.load_time)
    
    def get_range(self, target):
        arange = [target]
        arange = self.addBelow(target, arange)
        return arange

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
    def __init__(self):
        super(TypeThree, self).__init__(self.load_time)
    
    def get_range(self, target):
        arange = [target]
        arange = self.addBelow(target, arange)
        arange = self.addRight(target, arange)
        if (target+1) % Board._X != 0:
            arange = self.addBelow(target + 1, arange)
        return arange

class TypeFour(Artillery):
    # Four Targets
    #      -----
    #      |   |
    #  -------------
    #  |   | T |   |
    #  -------------
    #      |   |
    #      -----
    damage = 2
    load_time = 2
    cost = 3
    def __init__(self):
        super(TypeFour, self).__init__(self.load_time)
    
    def get_range(self, target):
        arange = [target]
        arange = self.addAbove(target, arange)
        arange = self.addBelow(target, arange)
        arange = self.addRight(target, arange)
        arange = self.addLeft(target, arange)
        return arange

INV_MAP = {0: TypeZero,
            1: TypeOne,
            2: TypeTwo,
            3: TypeThree,
            4: TypeFour}

