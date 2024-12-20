from enum import IntEnum


class Distribution(IntEnum):
    limit = 1
    pair = 2


class Rules:
    def __init__(self):
        self.broken: bool = False  # initialize rules as not broken
        self.selection_limit: int = 2
        self.reason: IntEnum | None = None

    def check_rules(self, selected_tiles: list):
        self.check_selection_limit(len(selected_tiles))
        self.check_pairs(selected_tiles)

    def check_selection_limit(self, num_selected: int):
        """Check if the selection limit is exceeded."""
        if num_selected > self.selection_limit:
            self.broken = True
            self.reason = Distribution(1)

    def check_pairs(self, selected_tiles: list):
        if len(selected_tiles) == 2 and selected_tiles[0].name != selected_tiles[1].name:
            self.broken = True
            self.reason = Distribution(2)
