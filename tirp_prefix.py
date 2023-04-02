from tiep import Tiep


class TIRPPrefix:
    """
    A prefix of Time intervals-related pattern (TIRP).
    """

    def __init__(self, tieps: list[list[Tiep]]):
        """
        :param tieps: a list that represents all the tieps of the pattern in lexicography order

        """
        self.tieps: list[list[Tiep]] = tieps
