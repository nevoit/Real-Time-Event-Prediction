import const
from sti_db import STIDB
from sti_series import STISeries
from tiep import Tiep
from time_point_series import TimePointSeries
from tirp import TIRP
from tirp_prefix import TIRPPrefix
from tirp_prefix_detection import TIRPPrefixDetection


class TIRPCompletion:
    def __init__(self, tirp: TIRP, sti_train_set: STIDB):
        self.tirp: TIRP = tirp

        # get the tiep order and ignore the ending tiep of the event of interest.
        # the assumption is the event ot interest ending tiep is always the last tiep
        self.tiep_order: list[list[Tiep]] = tirp.get_sorted_tieps()[:-1]
        self.tiep_prefixes: list[TIRPPrefix] = self._get_tirp_prefixes()
        self._detect_tirp_prefixes(sti_train_set)

    def _get_tirp_prefixes(self) -> list[TIRPPrefix]:
        # This function returns a list of TIRP prefixes
        tiep_prefixes = []
        for i in range(len(self.tiep_order)):
            tiep_prefixes.append(TIRPPrefix(tieps=self.tiep_order[:i + 1]))
        return tiep_prefixes

    def _detect_tirp_prefixes(self, sti_train_set: STIDB):
        # This function returns all detected instances per TIRP Prefix
        train_set_with_event: list[STISeries] = [s for s in sti_train_set.get_sti_series() if
                                                 s.is_symbol_in_series(const.EVENT_INDEX)]
        train_set_without_event: list[STISeries] = [s for s in sti_train_set.sti_series_list if
                                                    not s.is_symbol_in_series(const.EVENT_INDEX)]

        for i, tirp_prefix in enumerate(self.tiep_prefixes):
            if i == 0:
                # the first TIRP-prefix is not relevant for learning a model --
                # since there is no duration while using one tiep
                continue
            else:
                self._detect_tirp_prefix_for_db(tirp_prefix=tirp_prefix, db=train_set_with_event)
                self._detect_tirp_prefix_for_db(tirp_prefix=tirp_prefix, db=train_set_without_event)

    def _detect_tirp_prefix_for_db(self, tirp_prefix: TIRPPrefix, db: list[STISeries]):
        print('TIRP-Prefix: \n' + tirp_prefix.get_tieps_str())
        for sti_series in db:
            print('STI Series: \n' + sti_series.get_stis_str())
            time_point_series: TimePointSeries = sti_series.get_time_points()
            print('Time Point Series: \n' + time_point_series.get_tiep_str())
            tirp_pfx_detect = TIRPPrefixDetection(tirp_prefix=tirp_prefix)
            tirp_pfx_insts: list[TimePointSeries] = tirp_pfx_detect.detect(time_point_series=time_point_series)
            print(f'Instances {len(tirp_pfx_insts)}:')
            for inst in tirp_pfx_insts:
                print(inst.get_tiep_str())
        print()
