import const


class Tiep:
    """
    This class represents the time interval endpoint that comprised of time, type, symbol id, and the symbol instance id
    """

    def __init__(self, time: int, tiep_type: str, sym_id: int, sym_inst_id: int, var_id: int,
                 tiep_inst_id: int = -1, dummy: bool = False):
        """
        :param time: the time of occurrence
        :param tiep_type: starting or ending endpoint
        :param sym_id: the symbol id
        :param sym_inst_id: the occurrence index of the same tiep in the series
        :param var_id: the variable id
        :param dummy: whether this object represents a dummy tiep (True) or real instances (False).
        """
        self._time: int = time
        self._tiep_type: str = tiep_type
        self._sym_id: int = sym_id
        self._var_id: int = var_id
        self._sym_inst_id: int = sym_inst_id  # each instance of this tiep should get the STI id
        self._tiep_inst_id: int = tiep_inst_id  # each instance of this tiep should get different id
        self._pair_tiep = None
        self._dummy: bool = dummy
        self._check_input_validity()

    def add_pair_tiep(self, tiep):
        self._pair_tiep: Tiep = tiep

    def get_pair_tiep(self):
        return self._pair_tiep

    def get_time(self) -> int:
        return self._time

    def get_tiep_type(self) -> str:
        return self._tiep_type

    def get_symbol_id(self) -> int:
        return self._sym_id

    def get_var_id(self) -> int:
        return self._var_id

    def get_symbol_instance_id(self) -> int:
        return self._sym_inst_id

    def get_tiep_instance_id(self) -> int:
        return self._tiep_inst_id

    def is_start_type(self) -> bool:
        # returns True if this is starting tiep
        return self._tiep_type == const.START_TIEP

    def is_end_type(self) -> bool:
        # returns True if this is ending tiep
        return self._tiep_type == const.END_TIEP

    def is_same_tiep(self, tp) -> bool:
        # this function gets another tiep and return True if they have the same type and symbol id
        if self._tiep_type == tp.get_tiep_type() and self._sym_id == tp.get_symbol_id():
            return True
        else:
            return False

    def is_same_tiep_instance(self, tp) -> bool:
        # this function gets an instances of another tiep and return True
        # if they have the same type, symbol id, instance id and variable id
        if self._tiep_type == tp.get_tiep_type() and self._sym_id == tp.get_symbol_id() \
                and self._sym_inst_id == tp.get_symbol_instance_id() and self._var_id == tp.get_var_id():
            return True
        else:
            return False

    def _check_input_validity(self):
        # this function check the validity of the input and assert in case of wrong input
        if not self._dummy and not self._time >= 0:
            assert "The provided time should be greater than zero!"
        elif self._tiep_type not in {const.START_TIEP, const.END_TIEP}:
            assert "The provided type should be '+' or '-'!"
        elif not self._sym_id >= 0:
            assert "The symbol id should be greater than zero!"
        elif not self._dummy and not self._var_id >= 0:
            assert "The variable id should be greater than zero!"
        elif not self._sym_inst_id >= 0:
            assert "The symbol instance id should be greater than zero!"
