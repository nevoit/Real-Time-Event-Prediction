from sti import STI
from tiep_series import TiepSeries
from time_point_series import TimePointSeries


class STISeries:
    """
    Lexicographical order symbolic time series
    """

    def __init__(self, series_id: int, stis_list: list):
        self.series_id: int = series_id
        self.stis: list = self._sort_sti_list(stis_list)
        self.tieps: TiepSeries = TiepSeries(stis_list=stis_list)
        self.time_points: TimePointSeries = TimePointSeries(tiep_series=self.tieps)
        self._check_input_validity()

    def get_time_points(self):
        return self.time_points

    def _sort_sti_list(self, stis_list):
        return sorted(stis_list, key=self.sort_sti)

    @staticmethod
    def sort_sti(sti):
        # Sort symbolic time intervals by lexicographical order
        return (sti.get_start_time(), sti.get_end_time(),
                sti.get_symbol_id(), sti.get_symbol_instance_id())

    def is_symbol_in_series(self, symbol_id) -> bool:
        # return whether an symbol id is included in the series
        for sti in self.stis:
            if sti.get_symbol_id() == symbol_id:
                return True
        return False

    def _check_input_validity(self):
        # This function check the validity of the input and assert in case of wrong input
        if self.series_id >= 0:
            assert "The series id should be greater than zero!"
        elif not len(self.stis) >= 0:
            assert "The STIs list should be greater than zero!"
