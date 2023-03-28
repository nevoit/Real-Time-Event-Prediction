from tiep_series import TiepSeries
from time_point import TimePoint


class TimePointSeries:
    def __init__(self, tiep_series: TiepSeries):
        self.time_point_series = self._create_time_point_series(tiep_series)

    @staticmethod
    def _create_time_point_series(tiep_series: TiepSeries) -> dict[int:TimePoint]:
        time_point_series = {}
        for tiep in tiep_series.get_tiep_list():
            if tiep.time not in time_point_series:
                time_point_series[tiep.time] = TimePoint(time=tiep.time)
            time_point_series[tiep.time].add_tiep(tiep)
        return time_point_series

    def get_time_point_series(self):
        return self.time_point_series
