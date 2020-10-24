class Cell:
    def __init__(self):
        self._visibility = 0

    def isVisible(self):
        return self._visibility > 0

    def update(self):
        if self.isVisible():
            self._visibility -= 1
    
    def dissipate(self):
        self._visibility = 3

    def __repr__(self):
        if self.isVisible():
            return " "
        else:
            return "X"

class Board:
    #  ----------------
    #  |0  1  2  3  4 |
    #  |5  6  7  8  9 |
    #  |10 11 12 13 14|
    #  |15 16 17 18 19|
    #  |20 21 22 23 24|
    #  ----------------
    _X = 5
    _Y = 5
    
    def __init__(self, mode = 'default'):
        if mode == 'default':
            self._board = self._normal_init()

    def _normal_init(self):
        board = []
        for i in range(self._X * self._Y):
            board.append(Cell())
        return board
        
    def __getitem__(self, key):
        return self._board[key]

    def update(self):
        for i in range(self._X * self._Y):
            self._board[i].update()

    def draw(self):
        i = 0
        for _ in range(self._Y):
            for _ in range(self._X):
                print(self._board[i], end='')
                i += 1
            print()



b = Board()
for i in range(25):
    assert not b[i].isVisible()


if __name__ == "__main__":
    b[6].dissipate()
    b.draw()

    print()
    b.update()
    b.update()
    b.update()
    b.draw()