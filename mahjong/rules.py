class Rules:
    def __init__(self):
        self.broken: bool = False  # initialize rules as not broken
        self.selection_limit: int = 2
        self.reason: str | None = None

    def check_rules(self, num_selected: int):
        self.check_selection_limit(num_selected)

    def check_selection_limit(self, num_selected: int):
        if num_selected > self.selection_limit:
            self.broken = True
            self.reason = "More than two tiles were selected."
