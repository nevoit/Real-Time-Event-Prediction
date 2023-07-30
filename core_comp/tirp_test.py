import unittest

import const
from core_comp.tirp import TIRP


class TestTIRP(unittest.TestCase):

    def test_sorted_tieps(self):
        """
        This function tests the sorted tieps compared to the TIRP's STIs and their temporal relations
        :return:
        """
        # Temporal relations
        rel_b = const.TEMP_REL_BEFORE
        rel_m = const.TEMP_REL_MEETS
        rel_c = const.TEMP_REL_CONTAINS
        rel_e = const.TEMP_REL_EQUALS
        rel_f = const.TEMP_REL_FINISHED_BY
        rel_o = const.TEMP_REL_OVERLAPS
        rel_s = const.TEMP_REL_STARTS

        # Tiep
        tp_srt = const.START_TIEP
        tp_end = const.END_TIEP
        tp_rel = const.REL_TIEP

        self.assertEqual(TIRP(stis=[1, 4, 999], temp_rels=[rel_b, rel_b, rel_b],
                              vs=1, hs=1).get_tieps_str(),
                         f'{tp_srt}1{tp_rel}{tp_end}1{tp_rel}{tp_srt}4{tp_rel}{tp_end}4{tp_rel}{tp_srt}999{tp_rel}{tp_end}999')

        self.assertEqual(TIRP(stis=[1, 4, 999], temp_rels=[rel_c, rel_b, rel_b],
                              vs=1, hs=1).get_tieps_str(),
                         f'{tp_srt}1{tp_rel}{tp_srt}4{tp_rel}{tp_end}4{tp_rel}{tp_end}1{tp_rel}{tp_srt}999{tp_rel}{tp_end}999')

        self.assertEqual(TIRP(stis=[1, 5, 15, 999], temp_rels=[rel_c, rel_c, rel_b, rel_b, rel_b, rel_b],
                              vs=1, hs=1).get_tieps_str(),
                         f'{tp_srt}1{tp_rel}{tp_srt}5{tp_rel}{tp_end}5{tp_rel}{tp_srt}15{tp_rel}{tp_end}15{tp_rel}{tp_end}1{tp_rel}{tp_srt}999{tp_rel}{tp_end}999')

        self.assertEqual(TIRP(stis=[1, 6, 999], temp_rels=[rel_m, rel_b, rel_m],
                              vs=1, hs=1).get_tieps_str(),
                         f'{tp_srt}1{tp_rel}({tp_end}1{tp_srt}6){tp_rel}({tp_end}6{tp_srt}999){tp_rel}{tp_end}999')

        self.assertEqual(TIRP(stis=[1, 6, 999], temp_rels=[rel_f, rel_b, rel_b],
                              vs=1, hs=1).get_tieps_str(),
                         f'{tp_srt}1{tp_rel}{tp_srt}6{tp_rel}({tp_end}1{tp_end}6){tp_rel}{tp_srt}999{tp_rel}{tp_end}999')

        self.assertEqual(TIRP(stis=[1, 6, 15, 999], temp_rels=[rel_c, rel_c, rel_e, rel_b, rel_b, rel_b],
                              vs=1, hs=1).get_tieps_str(),
                         f'{tp_srt}1{tp_rel}({tp_srt}6{tp_srt}15){tp_rel}({tp_end}6{tp_end}15){tp_rel}{tp_end}1{tp_rel}{tp_srt}999{tp_rel}{tp_end}999')

        self.assertEqual(TIRP(stis=[1, 24, 999], temp_rels=[rel_e, rel_b, rel_b],
                              vs=1, hs=1).get_tieps_str(),
                         f'({tp_srt}1{tp_srt}24){tp_rel}({tp_end}1{tp_end}24){tp_rel}{tp_srt}999{tp_rel}{tp_end}999')

        self.assertEqual(TIRP(stis=[1, 33, 6, 999], temp_rels=[rel_f, rel_c, rel_c, rel_b, rel_b, rel_b],
                              vs=1, hs=1).get_tieps_str(),
                         f'{tp_srt}1{tp_rel}{tp_srt}33{tp_rel}{tp_srt}6{tp_rel}{tp_end}6{tp_rel}({tp_end}1{tp_end}33){tp_rel}{tp_srt}999{tp_rel}{tp_end}999')

        self.assertEqual(TIRP(stis=[2, 5, 20, 23, 999],
                              temp_rels=[rel_b, rel_b, rel_b, rel_b, rel_b, rel_e, rel_b, rel_b, rel_b, rel_b],
                              vs=1, hs=1).get_tieps_str(),
                         f'{tp_srt}2{tp_rel}{tp_end}2{tp_rel}{tp_srt}5{tp_rel}{tp_end}5{tp_rel}({tp_srt}20{tp_srt}23){tp_rel}({tp_end}20{tp_end}23){tp_rel}{tp_srt}999{tp_rel}{tp_end}999')

        self.assertEqual(TIRP(stis=[2, 6, 10, 999], temp_rels=[rel_b, rel_b, rel_m, rel_b, rel_b, rel_b],
                              vs=1, hs=1).get_tieps_str(),
                         f'{tp_srt}2{tp_rel}{tp_end}2{tp_rel}{tp_srt}6{tp_rel}({tp_end}6{tp_srt}10){tp_rel}{tp_end}10{tp_rel}{tp_srt}999{tp_rel}{tp_end}999')

        self.assertEqual(TIRP(stis=[2, 6, 10, 999], temp_rels=[rel_b, rel_b, rel_s, rel_b, rel_b, rel_b],
                              vs=1, hs=1).get_tieps_str(),
                         f'{tp_srt}2{tp_rel}{tp_end}2{tp_rel}({tp_srt}6{tp_srt}10){tp_rel}{tp_end}6{tp_rel}{tp_end}10{tp_rel}{tp_srt}999{tp_rel}{tp_end}999')

        self.assertEqual(TIRP(stis=[2, 6, 999], temp_rels=[rel_b, rel_b, rel_m],
                              vs=1, hs=1).get_tieps_str(),
                         f'{tp_srt}2{tp_rel}{tp_end}2{tp_rel}{tp_srt}6{tp_rel}({tp_end}6{tp_srt}999){tp_rel}{tp_end}999')

        self.assertEqual(TIRP(stis=[2, 27, 6, 999], temp_rels=[rel_s, rel_b, rel_c, rel_b, rel_b, rel_b],
                              vs=1, hs=1).get_tieps_str(),
                         f'({tp_srt}2{tp_srt}27){tp_rel}{tp_end}2{tp_rel}{tp_srt}6{tp_rel}{tp_end}6{tp_rel}{tp_end}27{tp_rel}{tp_srt}999{tp_rel}{tp_end}999')

        self.assertEqual(TIRP(stis=[2, 33, 6, 999], temp_rels=[rel_o, rel_b, rel_c, rel_b, rel_b, rel_b],
                              vs=1, hs=1).get_tieps_str(),
                         f'{tp_srt}2{tp_rel}{tp_srt}33{tp_rel}{tp_end}2{tp_rel}{tp_srt}6{tp_rel}{tp_end}6{tp_rel}{tp_end}33{tp_rel}{tp_srt}999{tp_rel}{tp_end}999')

        self.assertEqual(TIRP(stis=[2, 33, 21, 999], temp_rels=[rel_o, rel_b, rel_f, rel_b, rel_b, rel_b],
                              vs=1, hs=1).get_tieps_str(),
                         f'{tp_srt}2{tp_rel}{tp_srt}33{tp_rel}{tp_end}2{tp_rel}{tp_srt}21{tp_rel}({tp_end}33{tp_end}21){tp_rel}{tp_srt}999{tp_rel}{tp_end}999')


if __name__ == '__main__':
    unittest.main()
