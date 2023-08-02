from core_comp.sti import STI
from core_comp.tiep import Tiep


class TiepSeries:
    """
    Lexicographical order symbolic time series endpoints (tiep)
    """

    def __init__(self, stis_list: list[STI]):
        self._tiep_list: list[Tiep] = self._create_sorted_tiep_series(stis_list)
        self._check_input_validity()

    def _create_sorted_tiep_series(self, stis_list) -> list[Tiep]:
        # this function creates sorted tiep series
        tiep_list = []
        for sti in stis_list:
            tiep_list.append(sti._start_tiep)
            tiep_list.append(sti._end_tiep)

        return self._sort_tiep_list(tiep_list=tiep_list)

    def _sort_tiep_list(self, tiep_list: list[Tiep]) -> list[Tiep]:
        return sorted(tiep_list, key=self.sort_tiep)

    @staticmethod
    def sort_tiep(tiep: Tiep):
        # sort symbolic time intervals by lexicographical order
        return (tiep.get_time(), tiep.get_symbol_id(), tiep.get_symbol_instance_id(), tiep.get_tiep_type())

    def get_tiep_list(self):
        return self._tiep_list

    def _check_input_validity(self):
        # this function check the validity of the input and assert in case of wrong input
        if not len(self._tiep_list) >= 0:
            assert "The STIs list should be greater than zero!"
