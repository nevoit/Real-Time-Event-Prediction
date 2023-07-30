import unittest

import const
from core_comp.sti import STI
from core_comp.sti_series import STISeries
from core_comp.tiep import Tiep
from core_comp.time_point_series import TimePointSeries
from tirp_prefix import TIRPrefix
from tirp_prefix_detection import TIRPrefixDetection


class TestTIRPPrefixDetection(unittest.TestCase):

    def test_three_tieps_d_prefix(self):
        """
        TIRP-Prefix:
        (+1+2)<-1<-2

        STI Series:
         ----1-----
         -----2-------
                      -1--
                             1--

        Time Point Series:
        (+1+2[5])<-1[15]<(+1-2[18])<-1[22]<+1[25]<-1[28]
        """
        tieps: list[list[Tiep]] = [
            [self._create_dummy_tiep(tiep_type=const.START_TIEP, sym_id=1, sym_inst_id=2, var_id=1, tiep_inst_id=1),
             self._create_dummy_tiep(tiep_type=const.START_TIEP, sym_id=2, sym_inst_id=1, var_id=1, tiep_inst_id=1)],
            [self._create_dummy_tiep(tiep_type=const.END_TIEP, sym_id=1, sym_inst_id=1, var_id=1, tiep_inst_id=2)],
            [self._create_dummy_tiep(tiep_type=const.END_TIEP, sym_id=2, sym_inst_id=3, var_id=1, tiep_inst_id=3)]
        ]

        stis_list: list[STI] = [
            self._create_sti_instance(start_time=5, end_time=18, sym_id=2, sym_inst_id=1, var_id=1),
            self._create_sti_instance(start_time=5, end_time=15, sym_id=1, sym_inst_id=2, var_id=1),
            self._create_sti_instance(start_time=18, end_time=22, sym_id=1, sym_inst_id=3, var_id=1),
            self._create_sti_instance(start_time=25, end_time=28, sym_id=1, sym_inst_id=4, var_id=1),
        ]

        expected_instances = {'(+1+2[5])<-1[15]<-2[18]'}  # TODO: think about lexigorapical order with these tieps

        tirp_prefix = TIRPrefix(tieps=tieps)
        sti_series = STISeries(series_id=0, stis_list=stis_list)
        self._format_for_tirp_prefix_detection(tirp_prefix=tirp_prefix,
                                               sti_series=sti_series,
                                               expected_instances=set(expected_instances))

    def test_three_tieps_c_prefix(self):
        """
        TIRP-Prefix:
        (+2+1)<-1<-2

        STI Series:
          --2---
          ----1-----
                          -1--
                                --1---

        Time Point Series:
        +2[2]<+1[5]<-2[8]<-1[15]<+1[18]<-1[22]<+1[25]<-1[28]
        """
        tieps: list[list[Tiep]] = [
            [self._create_dummy_tiep(tiep_type=const.START_TIEP, sym_id=2, sym_inst_id=1, var_id=1, tiep_inst_id=1),
             self._create_dummy_tiep(tiep_type=const.START_TIEP, sym_id=1, sym_inst_id=2, var_id=1, tiep_inst_id=1)],
            [self._create_dummy_tiep(tiep_type=const.END_TIEP, sym_id=1, sym_inst_id=1, var_id=1, tiep_inst_id=2)],
            [self._create_dummy_tiep(tiep_type=const.END_TIEP, sym_id=2, sym_inst_id=3, var_id=1, tiep_inst_id=3)]
        ]

        stis_list: list[STI] = [
            self._create_sti_instance(start_time=5, end_time=16, sym_id=2, sym_inst_id=1, var_id=1),
            self._create_sti_instance(start_time=5, end_time=15, sym_id=1, sym_inst_id=2, var_id=1),
            self._create_sti_instance(start_time=18, end_time=22, sym_id=1, sym_inst_id=3, var_id=1),
            self._create_sti_instance(start_time=25, end_time=28, sym_id=1, sym_inst_id=4, var_id=1),
        ]

        expected_instances = {'(+2+1[5])<-1[15]<-2[16]'}  # TODO: think about lexigorapical order with these tieps

        tirp_prefix = TIRPrefix(tieps=tieps)
        sti_series = STISeries(series_id=0, stis_list=stis_list)
        self._format_for_tirp_prefix_detection(tirp_prefix=tirp_prefix,
                                               sti_series=sti_series,
                                               expected_instances=set(expected_instances))

    def test_three_tieps_b_prefix(self):
        """
        TIRP-Prefix:
        +1<-1<+1

        STI Series:
          --2---
             ----1-----
                          -1--
                                --1---

        Time Point Series:
        +2[2]<+1[5]<-2[8]<-1[15]<+1[18]<-1[22]<+1[25]<-1[28]
        """
        tieps: list[list[Tiep]] = [
            [self._create_dummy_tiep(tiep_type=const.START_TIEP, sym_id=1, sym_inst_id=1, var_id=1, tiep_inst_id=1)],
            [self._create_dummy_tiep(tiep_type=const.END_TIEP, sym_id=1, sym_inst_id=1, var_id=1, tiep_inst_id=2)],
            [self._create_dummy_tiep(tiep_type=const.START_TIEP, sym_id=1, sym_inst_id=2, var_id=1, tiep_inst_id=3)],
        ]

        stis_list: list[STI] = [
            self._create_sti_instance(start_time=2, end_time=8, sym_id=2, sym_inst_id=1, var_id=1),
            self._create_sti_instance(start_time=5, end_time=15, sym_id=1, sym_inst_id=2, var_id=1),
            self._create_sti_instance(start_time=18, end_time=22, sym_id=1, sym_inst_id=3, var_id=1),
            self._create_sti_instance(start_time=25, end_time=28, sym_id=1, sym_inst_id=4, var_id=1),
        ]

        expected_instances = {'+1[18]<-1[22]<+1[25]', '+1[5]<-1[15]<+1[25]', '+1[5]<-1[15]<+1[18]'}

        tirp_prefix = TIRPrefix(tieps=tieps)
        sti_series = STISeries(series_id=0, stis_list=stis_list)
        self._format_for_tirp_prefix_detection(tirp_prefix=tirp_prefix,
                                               sti_series=sti_series,
                                               expected_instances=set(expected_instances))

    def test_four_tieps_c_prefix(self):
        """
        TIRP-Prefix:
        +2<+1<-2<-1

        STI Series:
          --2---
             ----1-----
                          -1--
                                --1---

        Time Point Series:
        +2[2]<+1[5]<-2[8]<-1[15]<+1[18]<-1[22]<+1[25]<-1[28]
        """
        tieps: list[list[Tiep]] = [
            [self._create_dummy_tiep(tiep_type=const.START_TIEP, sym_id=1, sym_inst_id=1, var_id=1, tiep_inst_id=1)],
            [self._create_dummy_tiep(tiep_type=const.END_TIEP, sym_id=1, sym_inst_id=1, var_id=1, tiep_inst_id=2)],
            [self._create_dummy_tiep(tiep_type=const.START_TIEP, sym_id=1, sym_inst_id=2, var_id=1, tiep_inst_id=3)],
            [self._create_dummy_tiep(tiep_type=const.END_TIEP, sym_id=1, sym_inst_id=3, var_id=1, tiep_inst_id=4)],
        ]

        stis_list: list[STI] = [
            self._create_sti_instance(start_time=2, end_time=8, sym_id=2, sym_inst_id=1, var_id=1),
            self._create_sti_instance(start_time=5, end_time=15, sym_id=1, sym_inst_id=2, var_id=1),
            self._create_sti_instance(start_time=18, end_time=22, sym_id=1, sym_inst_id=3, var_id=1),
            self._create_sti_instance(start_time=25, end_time=28, sym_id=1, sym_inst_id=4, var_id=1),
        ]

        expected_instances = {'+1[5]<-1[15]<+1[18]<-1[22]', '+1[18]<-1[22]<+1[25]<-1[28]', '+1[5]<-1[15]<+1[25]<-1[28]'}

        tirp_prefix = TIRPrefix(tieps=tieps)
        sti_series = STISeries(series_id=0, stis_list=stis_list)
        self._format_for_tirp_prefix_detection(tirp_prefix=tirp_prefix,
                                               sti_series=sti_series,
                                               expected_instances=set(expected_instances))

    def test_four_tieps_b_prefix(self):
        """
        TIRP-Prefix:
        +1<-1<+1<-1

        STI Series:
          --2---
             ----1-----
                          -1--
                                --1---

        Time Point Series:
        +2[2]<+1[5]<-2[8]<-1[15]<+1[18]<-1[22]<+1[25]<-1[28]
        """
        tieps: list[list[Tiep]] = [
            [self._create_dummy_tiep(tiep_type=const.START_TIEP, sym_id=1, sym_inst_id=1, var_id=1, tiep_inst_id=1)],
            [self._create_dummy_tiep(tiep_type=const.END_TIEP, sym_id=1, sym_inst_id=1, var_id=1, tiep_inst_id=2)],
            [self._create_dummy_tiep(tiep_type=const.START_TIEP, sym_id=1, sym_inst_id=2, var_id=1, tiep_inst_id=3)],
            [self._create_dummy_tiep(tiep_type=const.END_TIEP, sym_id=1, sym_inst_id=3, var_id=1, tiep_inst_id=4)],
        ]

        stis_list: list[STI] = [
            self._create_sti_instance(start_time=2, end_time=8, sym_id=2, sym_inst_id=1, var_id=1),
            self._create_sti_instance(start_time=5, end_time=15, sym_id=1, sym_inst_id=2, var_id=1),
            self._create_sti_instance(start_time=18, end_time=22, sym_id=1, sym_inst_id=3, var_id=1),
            self._create_sti_instance(start_time=25, end_time=28, sym_id=1, sym_inst_id=4, var_id=1),
        ]

        expected_instances = {'+1[5]<-1[15]<+1[18]<-1[22]', '+1[18]<-1[22]<+1[25]<-1[28]', '+1[5]<-1[15]<+1[25]<-1[28]'}

        tirp_prefix = TIRPrefix(tieps=tieps)
        sti_series = STISeries(series_id=0, stis_list=stis_list)
        self._format_for_tirp_prefix_detection(tirp_prefix=tirp_prefix,
                                               sti_series=sti_series,
                                               expected_instances=set(expected_instances))

    def test_six_tieps_a_prefix(self):
        """
        TIRP-Prefix:
        +2<+1<-2<-1<+1<-1

        STI Series:
          --2---
             ----1-----
                          -1--

        Time Point Series:
        +2[2]+1[5]<-2[8]<-1[15]<+1[18]<-1[22]<
        """
        tieps: list[list[Tiep]] = [
            [self._create_dummy_tiep(tiep_type=const.START_TIEP, sym_id=2, sym_inst_id=1, var_id=1, tiep_inst_id=1)],
            [self._create_dummy_tiep(tiep_type=const.START_TIEP, sym_id=1, sym_inst_id=2, var_id=1, tiep_inst_id=2)],
            [self._create_dummy_tiep(tiep_type=const.END_TIEP, sym_id=2, sym_inst_id=1, var_id=1, tiep_inst_id=3)],
            [self._create_dummy_tiep(tiep_type=const.END_TIEP, sym_id=1, sym_inst_id=2, var_id=1, tiep_inst_id=4)],
            [self._create_dummy_tiep(tiep_type=const.START_TIEP, sym_id=1, sym_inst_id=3, var_id=1, tiep_inst_id=5)],
            [self._create_dummy_tiep(tiep_type=const.END_TIEP, sym_id=1, sym_inst_id=3, var_id=1, tiep_inst_id=6)],
        ]

        stis_list: list[STI] = [
            self._create_sti_instance(start_time=2, end_time=8, sym_id=2, sym_inst_id=1, var_id=1),
            self._create_sti_instance(start_time=5, end_time=15, sym_id=1, sym_inst_id=2, var_id=1),
            self._create_sti_instance(start_time=18, end_time=22, sym_id=1, sym_inst_id=3, var_id=1),
        ]

        expected_instances = {'+2[2]<+1[5]<-2[8]<-1[15]<+1[18]<-1[22]'}

        tirp_prefix = TIRPrefix(tieps=tieps)
        sti_series = STISeries(series_id=0, stis_list=stis_list)
        self._format_for_tirp_prefix_detection(tirp_prefix=tirp_prefix,
                                               sti_series=sti_series,
                                               expected_instances=set(expected_instances))

    def test_four_tieps_a_prefix(self):
        """
        TIRP-Prefix:
        +2<+1<-2<-1

        STI Series:
          --2---
             ----1-----
                          -1--

        Time Point Series:
        +2[2]+1[5]<-2[8]<-1[15]<+1[18]<-1[22]<
        """
        tieps: list[list[Tiep]] = [
            [self._create_dummy_tiep(tiep_type=const.START_TIEP, sym_id=2, sym_inst_id=1, var_id=1, tiep_inst_id=1)],
            [self._create_dummy_tiep(tiep_type=const.START_TIEP, sym_id=1, sym_inst_id=2, var_id=1, tiep_inst_id=2)],
            [self._create_dummy_tiep(tiep_type=const.END_TIEP, sym_id=2, sym_inst_id=1, var_id=1, tiep_inst_id=3)],
            [self._create_dummy_tiep(tiep_type=const.END_TIEP, sym_id=1, sym_inst_id=2, var_id=1, tiep_inst_id=4)],
        ]

        stis_list: list[STI] = [
            self._create_sti_instance(start_time=2, end_time=8, sym_id=2, sym_inst_id=1, var_id=1),
            self._create_sti_instance(start_time=5, end_time=15, sym_id=1, sym_inst_id=2, var_id=1),
            self._create_sti_instance(start_time=18, end_time=22, sym_id=1, sym_inst_id=3, var_id=1),
        ]

        expected_instances = {'+2[2]<+1[5]<-2[8]<-1[15]'}

        tirp_prefix = TIRPrefix(tieps=tieps)
        sti_series = STISeries(series_id=0, stis_list=stis_list)
        self._format_for_tirp_prefix_detection(tirp_prefix=tirp_prefix,
                                               sti_series=sti_series,
                                               expected_instances=set(expected_instances))

    def test_three_tieps_a_prefix(self):
        """
        TIRP-Prefix:
        +2<+1<-1

        STI Series:
          --2---
             ----1-----
                          -1--

        Time Point Series:
        +2[2]+1[5]<-2[8]<-1[15]<+1[18]<-1[22]<
        """
        tieps: list[list[Tiep]] = [
            [self._create_dummy_tiep(tiep_type=const.START_TIEP, sym_id=2, sym_inst_id=1, var_id=1, tiep_inst_id=1)],
            [self._create_dummy_tiep(tiep_type=const.START_TIEP, sym_id=1, sym_inst_id=2, var_id=1, tiep_inst_id=2)],
            [self._create_dummy_tiep(tiep_type=const.END_TIEP, sym_id=1, sym_inst_id=2, var_id=1, tiep_inst_id=3)],
        ]

        stis_list: list[STI] = [
            self._create_sti_instance(start_time=2, end_time=8, sym_id=2, sym_inst_id=1, var_id=1),
            self._create_sti_instance(start_time=5, end_time=15, sym_id=1, sym_inst_id=2, var_id=1),
            self._create_sti_instance(start_time=18, end_time=22, sym_id=1, sym_inst_id=3, var_id=1),
        ]

        expected_instances = {}

        tirp_prefix = TIRPrefix(tieps=tieps)
        sti_series = STISeries(series_id=0, stis_list=stis_list)
        self._format_for_tirp_prefix_detection(tirp_prefix=tirp_prefix,
                                               sti_series=sti_series,
                                               expected_instances=set(expected_instances))

    def test_two_tieps_a_prefix(self):
        """
        TIRP-Prefix:
        +1<-1

        STI Series:
          --2---
             ----1-----
                          -1--

        Time Point Series:
        +2[2]+1[5]<-2[8]<-1[15]<+1[18]<-1[22]<
        """
        tieps: list[list[Tiep]] = [
            [self._create_dummy_tiep(tiep_type=const.START_TIEP, sym_id=1, sym_inst_id=1, var_id=1, tiep_inst_id=1)],
            [self._create_dummy_tiep(tiep_type=const.END_TIEP, sym_id=1, sym_inst_id=1, var_id=1, tiep_inst_id=1)],
        ]

        stis_list: list[STI] = [
            self._create_sti_instance(start_time=2, end_time=8, sym_id=2, sym_inst_id=1, var_id=1),
            self._create_sti_instance(start_time=5, end_time=15, sym_id=1, sym_inst_id=2, var_id=1),
            self._create_sti_instance(start_time=18, end_time=22, sym_id=1, sym_inst_id=3, var_id=1),
        ]

        expected_instances = {'+1[18]<-1[22]', '+1[5]<-1[15]'}

        tirp_prefix = TIRPrefix(tieps=tieps)
        sti_series = STISeries(series_id=0, stis_list=stis_list)
        self._format_for_tirp_prefix_detection(tirp_prefix=tirp_prefix,
                                               sti_series=sti_series,
                                               expected_instances=set(expected_instances))

    def _create_dummy_tiep(self, tiep_type, sym_id, sym_inst_id, var_id, tiep_inst_id) -> Tiep:
        tiep = Tiep(time=-1, tiep_type=tiep_type, sym_id=sym_id, sym_inst_id=sym_inst_id, var_id=var_id,
                    tiep_inst_id=tiep_inst_id, dummy=True)
        return tiep

    def _create_sti_instance(self, start_time, end_time, sym_id, sym_inst_id, var_id) -> STI:
        start_tiep = Tiep(time=start_time, tiep_type=const.START_TIEP, sym_id=sym_id, sym_inst_id=sym_inst_id,
                          var_id=var_id)
        end_tiep = Tiep(time=end_time, tiep_type=const.END_TIEP, sym_id=sym_id, sym_inst_id=sym_inst_id, var_id=var_id)
        start_tiep.add_pair_tiep(end_tiep)
        end_tiep.add_pair_tiep(start_tiep)

        return STI(start_tiep, end_tiep)

    def _format_for_tirp_prefix_detection(self, tirp_prefix: TIRPrefix, sti_series: STISeries,
                                          expected_instances: set):
        """
        This function check whether the expected instances of the TIRP-prefix were detected in the STI list
        :param tirp_prefix:
        :param sti_series:
        :param expected_instances:
        :return:
        """
        print('TIRP-Prefix: \n' + tirp_prefix.get_tieps_str())
        tirp_prefix_detection = TIRPrefixDetection(tirp_prefix=tirp_prefix)

        print('STI Series: \n' + sti_series.get_stis_str())
        time_point_series: TimePointSeries = sti_series.get_time_points()
        print('Time Point Series: \n' + time_point_series.get_tiep_str())

        tirp_pfx_insts: list[TimePointSeries] = tirp_prefix_detection.detect(sti_series_id=sti_series.get_series_id(),
                                                                             time_point_series=time_point_series)

        print(f'Instances {len(tirp_pfx_insts)}:')
        tirp_pfx_srt_insts = []
        for inst in tirp_pfx_insts:
            tirp_pfx_str = inst.get_tiep_str()
            tirp_pfx_srt_insts.append(tirp_pfx_str)
            print(tirp_pfx_str)
        tirp_pfx_srt_insts = set(tirp_pfx_srt_insts)

        print(tirp_pfx_srt_insts)
        print(expected_instances)
        self.assertSetEqual(tirp_pfx_srt_insts, expected_instances)


if __name__ == '__main__':
    unittest.main()
