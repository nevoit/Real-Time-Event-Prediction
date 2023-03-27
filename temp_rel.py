from sti import STI


class TempRel:
    """
    This class represents the Allen's seven temporal relations
    """

    def __init__(self, sti_a: STI, sti_b: STI):
        self.sti_a: STI = sti_a
        self.sti_b: STI = sti_b
        self._check_input_validity()

        self.rel = self._define_temp_rel()

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
        if self.sti_a.get_start_time() < self.sti_a.get_end_time() < self.sti_b.get_start_time() < self.sti_b.get_end_time():
            return 'b'  # b | before      | A+ < A- < B+ < B-
        elif self.sti_a.get_start_time() < self.sti_a.get_end_time() == self.sti_b.get_start_time() < self.sti_b.get_end_time():
            return 'm'  # m | meets       | A+ < A- = B+ < B-
        elif self.sti_a.get_start_time() < self.sti_b.get_start_time() < self.sti_a.get_end_time() < self.sti_b.get_end_time():
            return 'o'  # o | overlaps    | A+ < B+ < A- < B-
        elif self.sti_a.get_start_time() < self.sti_b.get_start_time() < self.sti_a.get_end_time() == self.sti_b.get_end_time():
            return 'f'  # f | finished-by | A+ < B+ < A- = B-
        elif self.sti_a.get_start_time() < self.sti_b.get_start_time() < self.sti_b.get_end_time() < self.sti_a.get_end_time():
            return 'c'  # c | contains    | A+ < B+ < B- < A-
        elif self.sti_a.get_start_time() == self.sti_b.get_start_time() < self.sti_a.get_end_time() < self.sti_b.get_end_time():
            return 's'  # s | starts      | A+ = B+ < A- < B-
        elif self.sti_a.get_start_time() == self.sti_b.get_start_time() < self.sti_a.get_end_time() == self.sti_b.get_end_time():
            return 'e'  # e | equals      | A+ = B+ < A- = B-

        assert "Error with the temporal relations"

    def _check_input_validity(self):
        # This function checks the validity of the input and assert in case of wrong input

        # makes sure that the lexicographical order between the STIs is valid
        if not self.sti_a.get_start_time() < self.sti_b.get_start_time():
            assert "Wrong lexicographic order! STI's A start tiep should start first"
        elif not ((self.sti_a.get_start_time() == self.sti_b.get_start_time()) and (
                self.sti_a.get_end_time() < self.sti_b.get_end_time())):
            assert "Wrong lexicographic order! STI's A end tiep should end first"
        elif not ((self.sti_a.get_start_time() == self.sti_b.get_start_time()) and (
                self.sti_a.get_end_time() == self.sti_b.get_end_time()) and (
                          self.sti_a.get_end_time() < self.sti_b.get_end_time())):
            assert "Wrong lexicographic order! STI's A symbol index should lower than B symbol index"

        """
        Wrong input (1):
        ---------A----------
                      -----A------
        
        Wrong input (2):
        ---------A----------|-----A------
        """
        if self.sti_a.get_symbol_id() == self.sti_b.get_symbol_id():
            if not self.sti_a.get_end_time() < self.sti_b.get_start_time():
                assert "Intervals with the same symbol id cannot overlap or meet"
