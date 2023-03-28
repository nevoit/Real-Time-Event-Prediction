from tiep import Tiep


class TimePoint:
    """
    Represent a time point with at least tiep
    """
    def __init__(self, time: int):
        self.time: int = time
        self.tieps: list[Tiep] = []

    def add_tiep(self, tiep):
        self.tieps.append(tiep)

    def get_time(self, time) -> int:
        return self.time