from sti import STI
import const


class TempRel:
    """
    This class represents the Allen's seven temporal relations
    """

    def __init__(self, sti_a: STI, sti_b: STI):
        self._sti_a: STI = sti_a
        self._sti_b: STI = sti_b
        self._check_input_validity()

        self._rel = self._define_temp_rel()

    def _define_temp_rel(self) -> str:
        """
        This function define the temporal relation of the seven temporal relations

        b | before      | A+ < A- < B+ < B-
        m | meets       | A+ < A- = B+ < B-
        o | overlaps    | A+ < B+ < A- < B-
        f | finished-by | A+ < B+ < A- = B-
        c | contains    | A+ < B+ < B- < A-
        s | starts      | A+ = B+ < A- < B-
        e | equals      | A+ = B+ < A- = B-

        :return:The Allen's temporal relation
        """
        if self._sti_a.get_start_time() < self._sti_a.get_end_time() < self._sti_b.get_start_time() < self._sti_b.get_end_time():
            return const.TEMP_REL_BEFORE  # b | before      | A+ < A- < B+ < B-
        elif self._sti_a.get_start_time() < self._sti_a.get_end_time() == self._sti_b.get_start_time() < self._sti_b.get_end_time():
            return const.TEMP_REL_MEETS  # m | meets       | A+ < A- = B+ < B-
        elif self._sti_a.get_start_time() < self._sti_b.get_start_time() < self._sti_a.get_end_time() < self._sti_b.get_end_time():
            return const.TEMP_REL_OVERLAPS  # o | overlaps    | A+ < B+ < A- < B-
        elif self._sti_a.get_start_time() < self._sti_b.get_start_time() < self._sti_a.get_end_time() == self._sti_b.get_end_time():
            return const.TEMP_REL_FINISHED_BY  # f | finished-by | A+ < B+ < A- = B-
        elif self._sti_a.get_start_time() < self._sti_b.get_start_time() < self._sti_b.get_end_time() < self._sti_a.get_end_time():
            return const.TEMP_REL_CONTAINS  # c | contains    | A+ < B+ < B- < A-
        elif self._sti_a.get_start_time() == self._sti_b.get_start_time() < self._sti_a.get_end_time() < self._sti_b.get_end_time():
            return const.TEMP_REL_STARTS  # s | starts      | A+ = B+ < A- < B-
        elif self._sti_a.get_start_time() == self._sti_b.get_start_time() < self._sti_a.get_end_time() == self._sti_b.get_end_time():
            return const.TEMP_REL_EQUALS  # e | equals      | A+ = B+ < A- = B-

        assert "Error with the temporal relations"

    def _check_input_validity(self):
        # This function checks the validity of the input and assert in case of wrong input
        # makes sure that the lexicographical order between the STIs is valid
        if not self._sti_a.get_start_time() < self._sti_b.get_start_time():
            assert "Wrong lexicographic order! STI's A start tiep should start first"
        elif not ((self._sti_a.get_start_time() == self._sti_b.get_start_time()) and (
                self._sti_a.get_end_time() < self._sti_b.get_end_time())):
            assert "Wrong lexicographic order! STI's A end tiep should end first"
        elif not ((self._sti_a.get_start_time() == self._sti_b.get_start_time()) and (
                self._sti_a.get_end_time() == self._sti_b.get_end_time()) and (
                          self._sti_a.get_end_time() < self._sti_b.get_end_time())):
            assert "Wrong lexicographic order! STI's A symbol index should lower than B symbol index"

        """
        Wrong input (1):
        ---------A----------
                      -----A------
        
        Wrong input (2):
        ---------A----------|-----A------
        """
        if self._sti_a.get_symbol_id() == self._sti_b.get_symbol_id():
            if not self._sti_a.get_end_time() < self._sti_b.get_start_time():
                assert "Intervals with the same symbol id cannot overlap or meet"
