import const
from sti_db import STIDB
from tiep import Tiep
from tirp import TIRP


class TIRPCompletion:
    def __init__(self, tirp: TIRP, sti_train_set: STIDB):
        self.tirp: TIRP = tirp

        # get the tiep order and ignore the ending tiep of the event of interest.
        # the assumption is the event ot interest ending tiep is always the last tiep
        self.tiep_order: list[list[Tiep]] = tirp.get_tieps()[:-1]

        self.sti_train_set: STIDB = sti_train_set

        self.train_set_with_event = [s for s in self.sti_train_set.get_sti_series() if
                                     s.is_symbol_in_series(const.EVENT_INDEX)]
        self.train_set_without_event = [s for s in self.sti_train_set.sti_series_list if
                                        not s.is_symbol_in_series(const.EVENT_INDEX)]
        print()
