import const
from core_comp.tiep import Tiep


class TIRPrefix:
    """
    A prefix of Time intervals-related pattern (TIRP).
    """

    def __init__(self, tieps: list[list[Tiep]]):
        """
        :param tieps: a list that represents all the tieps of the pattern in lexicography order

        """
        self._tieps: list[list[Tiep]] = tieps

    def get_tieps(self) -> list[list[Tiep]]:
        return self._tieps

    def get_tieps_str(self) -> str:
        # returns str representation of the TIRP prefix
        tiep_str = ''
        for i, tps in enumerate(self._tieps):
            if len(tps) > 1:
                tiep_str += '('
            for tp in tps:
                tiep_str += f'{tp._tiep_type}{tp._sym_id}'
            if len(tps) > 1:
                tiep_str += ')'
            if i != len(self._tieps) - 1:
                tiep_str += const.REL_TIEP
        return tiep_str