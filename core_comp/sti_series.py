import const
from sti import STI
from tiep_series import TiepSeries
from time_point_series import TimePointSeries


class STISeries:
    """
    Lexicographical order symbolic time series
    """

    def __init__(self, series_id: int, stis_list: list[STI]):
        self.series_id: int = series_id
        self.stis: list = self._sort_sti_list(stis_list)
        self.tieps: TiepSeries = TiepSeries(stis_list=stis_list)
        self.time_points: TimePointSeries = TimePointSeries(entity_id=series_id, tiep_series=self.tieps)
        self._check_input_validity()

    def get_stis_str(self):
        sti_str = ''
        for sti in self.stis:
            start_time = sti.get_start_time()
            end_time = sti.get_end_time()
            sym_id = str(sti.get_symbol_id())
            space_str = ' ' * start_time
            interval_str = '-' * (end_time - start_time)
            if len(interval_str) == 1:
                interval_str = sym_id
            else:
                str_to_replace_index = int(len(interval_str) / 2) - 1  # replace the middle char
                interval_str = "".join(
                    (interval_str[:str_to_replace_index], sym_id, interval_str[str_to_replace_index + len(sym_id):]))
            sti_str += f'{space_str}{interval_str} \n'
        return sti_str

    def get_first_sti_start_time(self) -> int:
        # This is used to get the event start time in entities with events
        first_sti: STI = self.stis[0]
        return first_sti.get_start_time()

    def get_last_sti_end_time(self) -> int:
        # This is used to get the event start time in entities with events
        last_sti: STI = self.stis[-1]
        if last_sti.get_symbol_id() == const.EVENT_INDEX:
            return last_sti.get_start_time()
        else:
            return last_sti.get_end_time()

    def get_start_to_end_time_timestamp_list(self) -> list:
        return list(range(self.get_first_sti_start_time(), self.get_last_sti_end_time()))

    def get_series_id(self):
        return self.series_id

    def get_tieps(self):
        return self.tieps

    def get_time_points(self):
        return self.time_points

    def get_time_points_at(self, until_time):
        # returns only time points that before the given time
        tps = self.time_points.get_time_point_series()
        time_point_series_at = TimePointSeries(entity_id=self.series_id)
        for tp in tps:
            if tp.get_time() < until_time:
                time_point_series_at.add_time_point(time_point=tp)
        return time_point_series_at

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
