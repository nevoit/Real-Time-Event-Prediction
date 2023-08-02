from core_comp.tiep import Tiep


class TimePoint:
    """
    represent a time point with at least tiep
    """
    def __init__(self, time: int, tieps: list[Tiep] = None):
        self._time: int = time
        if tieps is None:
            self._tieps: list[Tiep] = []
        else:
            self._tieps = tieps

    def add_tiep(self, tiep):
        self._tieps.append(tiep)

    def get_time(self) -> int:
        return self._time

    def get_tieps(self):
        return self._tieps

    def is_tiep_instance_exist(self, tiep_to_check: Tiep) -> bool:
        # this function gets a tiep and returns whether they have the same type and symbol
        for tiep in self._tieps:
            if tiep.is_same_tiep_instance(tiep_to_check):
                return True
        return False

    def get_tiep_str(self) -> str:
        # this function returns str representation of the time point
        tiep_str = ''
        if len(self._tieps) > 1:
            tiep_str += '('
        for tp in self._tieps:
            tiep_str += f'{tp._tiep_type}{tp._sym_id}'
        tiep_str += f'[{self._time}]'
        if len(self._tieps) > 1:
            tiep_str += ')'
        return tiep_str
