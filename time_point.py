from tiep import Tiep


class TimePoint:
    """
    Represent a time point with at least tiep
    """
    def __init__(self, time: int, tieps: list[Tiep] = None):
        self.time: int = time
        if tieps is None:
            self.tieps: list[Tiep] = []
        else:
            self.tieps = tieps

    def add_tiep(self, tiep):
        self.tieps.append(tiep)

    def get_time(self) -> int:
        return self.time

    def get_tieps(self):
        return self.tieps

    def is_tiep_instance_exist(self, tiep_to_check: Tiep):
        # This function gets a tiep and returns whether they have the same type and symbol
        for tiep in self.tieps:
            if tiep.is_same_tiep_instance(tiep_to_check):
                return True
        return False

    def get_tiep_str(self):
        tiep_str = ''
        if len(self.tieps) > 1:
            tiep_str += '('
        for tp in self.tieps:
            tiep_str += f'{tp.tiep_type}{tp.sym_id}'
        tiep_str += f'[{self.time}]'
        if len(self.tieps) > 1:
            tiep_str += ')'
        return tiep_str
