from core_comp.tiep import Tiep


class STI:
    """
    This class represents the symbolic time intervals that comprised of start and end tieps
    """

    def __init__(self, start_tiep: Tiep, end_tiep: Tiep):
        self._start_tiep: Tiep = start_tiep
        self._end_tiep: Tiep = end_tiep
        self._check_input_validity()

    def get_start_time(self) -> int:
        return self._start_tiep.get_time()

    def get_end_time(self) -> int:
        return self._end_tiep.get_time()

    def get_symbol_id(self) -> int:
        # Both start and end tiep have the same symbol
        return self._start_tiep.get_symbol_id()

    def get_var_id(self) -> int:
        # Both start and end tiep have the same var id
        return self._start_tiep.get_var_id()

    def get_symbol_instance_id(self) -> int:
        # Both start and end tiep have the same symbol instance index
        return self._start_tiep.get_symbol_instance_id()

    def _check_input_validity(self):
        # This function check the validity of the input and assert in case of wrong input
        if not self._start_tiep.is_start_type():
            assert "The provided start tiep has an incorrect type!"
        elif not self._end_tiep.is_end_type():
            assert "The provided end tiep has an incorrect type!"
        elif not self._start_tiep.get_time() < self._end_tiep.get_time():
            assert "The start tiep should start earlier to the end tiep"
        elif not self._start_tiep.get_symbol_id() == self._end_tiep.get_symbol_id():
            assert "The tieps should have the same symbols"
        elif not self._start_tiep.get_symbol_instance_id() == self._end_tiep.get_symbol_instance_id():
            assert "The tieps should have the same symbol indexes"

