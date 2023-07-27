import copy
from typing import Optional

from tiep import Tiep
from time_point import TimePoint
from time_point_series import TimePointSeries
from tirp_prefix import TIRPPrefix


class TIRPPrefixDetection:
    def __init__(self, tirp_prefix: TIRPPrefix):
        self.tirp_prefix: TIRPPrefix = tirp_prefix

    def _tieps_contain_in_tieps(self, tieps_x: list[Tiep], tieps_y: list[Tiep]) -> Optional[TimePoint]:
        # This function returns whether tieps_x are the contains in tieps_y
        time_point = TimePoint(time=tieps_y[0].get_time())
        for tp_x in tieps_x:
            con_tiep = self._tiep_contains_in_tieps(tiep=tp_x, tieps_list=tieps_y)
            if con_tiep is None:
                return None
            else:
                time_point.add_tiep(con_tiep)
        return time_point

    def _tiep_contains_in_tieps(self, tiep: Tiep, tieps_list: list[Tiep]) -> Optional[Tiep]:
        # This function return whether a tiep is contain in the tieps list
        for tp in tieps_list:
            if tp.is_same_tiep(tiep):
                return tp
        return None

    def _find_tieps_in_time_point(self, tieps: list[Tiep], time_point_series: TimePointSeries) -> list[TimePoint]:
        # This function finds instances of the tieps in the time point series
        tieps_inst = []
        for time_point in time_point_series.get_time_point_series():
            # we find all the tieps in the time point series that equals to the first pattern tiep
            con_tieps = self._tieps_contain_in_tieps(tieps_x=tieps, tieps_y=time_point.get_tieps())
            if con_tieps is not None:
                tieps_inst.append(con_tieps)  # add tieps
        return tieps_inst

    def detect(self, time_point_series: TimePointSeries) -> list[TimePointSeries]:
        """
        This function detects instances of the TIRP-prefix in the given sorted time point series.
        The function is making sure the unfinished STIs were not finished before the series was appeared.
        :param time_point_series:
        :return:
        """
        tirp_prefix_insts = []
        for tieps_i, tieps in enumerate(self.tirp_prefix.get_tieps()):  # iterates over the pattern tieps
            pot_tieps_to_extend = self._find_tieps_in_time_point(tieps=tieps, time_point_series=time_point_series)
            if tieps_i == 0:  # iterates over the first pattern's tieps
                for tp in pot_tieps_to_extend:
                    tps = TimePointSeries()
                    tps.add_time_point(tp)
                    tirp_prefix_insts.append(tps)
            else:  # check if the previous tieps can be extended
                extended_tirp_prefix_insts = []
                for pot_tp in pot_tieps_to_extend:
                    for prev_inst in tirp_prefix_insts:  # for the previous instances
                        if self._is_previous_tieps_can_be_extended(prev_inst=prev_inst, pot_tp=pot_tp):
                            new_inst: TimePointSeries = copy.deepcopy(prev_inst)
                            new_inst.add_time_point(pot_tp)
                            extended_tirp_prefix_insts.append(new_inst)
                tirp_prefix_insts = extended_tirp_prefix_insts
        return tirp_prefix_insts

    def _is_previous_tieps_can_be_extended(self, prev_inst: TimePointSeries, pot_tp: TimePoint) -> bool:
        # This function checks whether the previous instance (list of time points)
        # could be extended with the current time point
        new_tp_time = pot_tp.get_time()
        lst_prev_tp_time = prev_inst.get_last_time_point_time()
        if lst_prev_tp_time >= new_tp_time:  # if the new time point is before the last time point of the instance
            return False
        elif prev_inst.are_end_tieps_closed_their_start_tieps(time_point=pot_tp) and \
                prev_inst.are_kept_unfinished_stis(time_point=pot_tp):
            return True
        else:
            return False
