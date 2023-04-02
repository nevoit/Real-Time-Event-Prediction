import const
from sti_db import STIDB
from sti_series import STISeries
from tiep import Tiep
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

        for tirp_prefix in self.tiep_prefixes:
            self._detect_tirp_prefix_for_db(tirp_prefix=tirp_prefix, db=train_set_with_event)
            self._detect_tirp_prefix_for_db(tirp_prefix=tirp_prefix, db=train_set_without_event)

    def _detect_tirp_prefix_for_db(self, tirp_prefix: TIRPPrefix, db: list[STISeries]):
        for sti_series in db:
            tiep_series = sti_series.get_tieps()
            tirp_prefix_detection = TIRPPrefixDetection(tirp_prefix=tirp_prefix)
            tirp_prefix_detection.detect(tiep_series=tiep_series)
            print()
