import unittest

from tirp import TIRP


class TestTIRP(unittest.TestCase):

    def test_tiep_oreder(self):
        self.assertEqual(TIRP(stis=[1, 4, 999], temp_rels=['b', 'b', 'b'],
                              vs=1, hs=1).get_tieps_str(), '+1<-1<+4<-4<+999<-999')

        self.assertEqual(TIRP(stis=[1, 4, 999], temp_rels=['c', 'b', 'b'],
                              vs=1, hs=1).get_tieps_str(), '+1<+4<-4<-1<+999<-999')

        self.assertEqual(TIRP(stis=[1, 5, 15, 999], temp_rels=['c', 'c', 'b', 'b', 'b', 'b'],
                              vs=1, hs=1).get_tieps_str(), '+1<+5<-5<+15<-15<-1<+999<-999')

        self.assertEqual(TIRP(stis=[1, 6, 999], temp_rels=['m', 'b', 'm'],
                              vs=1, hs=1).get_tieps_str(), '+1<(-1+6)<(-6+999)<-999')

        self.assertEqual(TIRP(stis=[1, 6, 999], temp_rels=['f', 'b', 'b'],
                              vs=1, hs=1).get_tieps_str(), '+1<+6<(-1-6)<+999<-999')

        self.assertEqual(TIRP(stis=[1, 6, 15, 999], temp_rels=['c', 'c', 'e', 'b', 'b', 'b'],
                              vs=1, hs=1).get_tieps_str(), '+1<(+6+15)<(-6-15)<-1<+999<-999')


if __name__ == '__main__':
    unittest.main()
