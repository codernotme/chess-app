from square import Square

class Move:

    def __init__(self, initial: Square, final: Square):
        self.initial = initial
        self.final = final

    def __str__(self) -> str:
        return f'({self.initial.col}, {self.initial.row}) -> ({self.final.col}, {self.final.row})'

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Move):
            return False
        return self.initial == other.initial and self.final == other.final
