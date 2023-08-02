import const
from core_comp.tiep import Tiep
from core_comp.tiep_series import TiepSeries
from core_comp.time_point import TimePoint


class TimePointSeries:
    """
    Ordered time point series
    """
    def __init__(self, entity_id, tiep_series: TiepSeries = None):
        self._entity_id = entity_id
        if tiep_series is not None:
            self._time_point_series: list[TimePoint] = self._create_time_point_series(tiep_series)
        else:
            self._time_point_series: list[TimePoint] = []

    def get_entity_id(self):
        return self._entity_id

    def get_time_point_series(self) -> list[TimePoint]:
        return self._time_point_series

    def add_time_point(self, time_point: TimePoint):
        self._time_point_series.append(time_point)

    def get_last_time_point_time(self) -> int:
        # returns the time of the last time point in the time point series
        return self._time_point_series[-1].get_time()

    def get_durations_between_all_tieps(self) -> list[int]:
        # returns list of duration between the tieps
        dur_list = []
        for i in range(len(self._time_point_series) - 1):
            dur_list.append(self.get_duration_between_adj_tieps(i))
        return dur_list

    def get_duration_between_adj_tieps(self, first_tiep_index) -> int:
        # returns the duration between the given tiep and its follows tiep
        gp = self._time_point_series[first_tiep_index + 1].get_time() - self._time_point_series[first_tiep_index].get_time()
        return gp

    def is_tiep_instance_exist(self, tiep: Tiep) -> bool:
        # returns true if the given tiep exists in the time point series
        for tp in self._time_point_series:
            if tp.is_tiep_instance_exist(tiep):
                return True
        return False

    def are_end_tieps_closed_their_start_tieps(self, time_point: TimePoint) -> bool:
        # this function checks if an end tiep ends the last start tiep with the same symbol of the prev instance
        for tiep in time_point.get_tieps():
            if tiep.is_end_type():
                paired_start_tiep = tiep.get_pair_tiep()
                if not self.is_tiep_instance_exist(paired_start_tiep):
                    return False
        return True

    def are_kept_unfinished_stis(self, time_point: TimePoint) -> bool:
        # this function checks which STIs should be unfinished in the TIRP-prefix
        # and for each validate they will be unfinished in case of extension
        new_tp_time = time_point.get_time()
        for tp in self._time_point_series:
            for tiep in tp.get_tieps():
                if tiep.is_start_type():
                    # for each start tiep in the time point series, check if it should be unfinished:
                    # if it's end time is before the new time point time, it should be included in the series
                    paired_end_tiep = tiep.get_pair_tiep()
                    paired_end_tiep_time = paired_end_tiep.get_time()
                    if paired_end_tiep_time < new_tp_time and not self.is_tiep_instance_exist(paired_end_tiep):
                        return False
        return True

    def get_tiep_str(self) -> str:
        # returns a str representation of the tiep point series
        tiep_str = ''
        for i, time_point in enumerate(self._time_point_series):
            tiep_str += time_point.get_tiep_str()
            if i != len(self._time_point_series) - 1:
                tiep_str += const.REL_TIEP
        return tiep_str

    @staticmethod
    def _create_time_point_series(tiep_series: TiepSeries) -> list[TimePoint]:
        # This function creates time point series given tiep series
        time_point_series = {}
        for tiep in tiep_series.get_tiep_list():
            if tiep._time not in time_point_series:
                time_point_series[tiep._time] = TimePoint(time=tiep._time)
            time_point_series[tiep._time].add_tiep(tiep)
        return [time_point_series[key] for key in sorted(time_point_series.keys())]