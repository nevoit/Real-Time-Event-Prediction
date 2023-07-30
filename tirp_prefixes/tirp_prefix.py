import const
from core_comp.tiep import Tiep


class TIRPPrefix:
    """
    A prefix of Time intervals-related pattern (TIRP).
    """

    def __init__(self, tieps: list[list[Tiep]]):
        """
        :param tieps: a list that represents all the tieps of the pattern in lexicography order

        """
        self.tieps: list[list[Tiep]] = tieps

    def get_tieps(self):
        return self.tieps

    def get_tieps_str(self) -> str:
        tiep_str = ''
        for i, tps in enumerate(self.tieps):
            if len(tps) > 1:
                tiep_str += '('
            for tp in tps:
                tiep_str += f'{tp.tiep_type}{tp.sym_id}'
            if len(tps) > 1:
                tiep_str += ')'
            if i != len(self.tieps) - 1:
                tiep_str += const.REL_TIEP
        return tiep_str